import traceback

from schema import Schema, Use, Optional, Or

schema = Schema({
	"command": str,
	"channel": Or(str, None),
	"badges": Or({
		Optional("moderator"):  Or(Use(int), str),
		Optional("subscriber"): Or(Use(int), str),
		Optional("premium"):    Or(Use(int), str),
		Optional("turbo"):      Or(Use(int), str)
	}, dict, None),
    "tags": Or({
        Optional("badge-info"):                Or(str, None),
        Optional("client-nonce"):              str,
        Optional("color"):                     Or(str, None),
        Optional("display-name"):              str,
        Optional("emote-only"):                Or(Use(int), str, None),
        Optional("followers-only"):            Or(Use(int), str, None),
        Optional("emotes"):                    Or(None, str, dict),
        Optional("emote-sets"):                list,
        Optional("first-msg"):                 Or(Use(int), str),
        Optional("flags"):                     Or(str, None),
        Optional("id"):                        str,
        Optional("mod"):                       Or(Use(int), str),
        Optional("reply-parent-display-name"): str,
        Optional("reply-parent-msg-body"):     str,
        Optional("reply-parent-msg-id"):       str,
        Optional("reply-parent-user-id"):      Or(Use(int), str),
        Optional("reply-parent-user-login"):   str,
        Optional("target-msg-id"):             str,
        Optional("returning-chatter"):         Or(Use(int), str),
        Optional("room-id"):                   Or(Use(int), str, None),
        Optional("subscriber"):                Or(Use(int), str),
        Optional("tmi-sent-ts"):               Or(Use(int), str),
        Optional("turbo"):                     Or(Use(int), str),
        Optional("login"):                     str,
        Optional("msg-id"):                    str,
        Optional("slow"):                      Or(Use(int), str),
        Optional("system-msg"):                Or(str, None),
        Optional("user-id"):                   Or(Use(int), str),
        Optional("user-type"):                 Or(str, None)
    }, None),
    "source": Or({
        Optional("nick"): Or(str, None),
        Optional("host"): str
    }, None),
    #"command": {
		#"command":                       str,
        #Optional("isCapRequestEnabled"): bool,
        #Optional("botCommand"):          Or(str, None),
        #Optional("botCommandParams"):    Or(str, None)
    #},
    "message": Or(str, None)
})

# Parses an IRC message and returns a JSON object with the message's 
# component parts (command, channel, badges, tags, source (nick and host), message). 
# Expects function receive a single message at a time. (Twitch IRC server may 
# send one or more IRC messages in a single message.)
def msg_parser(message):
	parsed_message = {# Contains the component parts.
		"command": None,
		"channel": None,
		"badges": None,
		"tags": None,
		"source": None,
		"message": None
	}

	# The start index. Increments as we parse the IRC message.
	idx = 0 

	# The raw components of the IRC message.
	tags_component = source_component = command_component = parameters_component = None

	# If the message includes tags, get the tags component of the IRC message.
	if message[idx] == '@':# The message includes tags.
		endIdx = message.find(' ')
		tags_component = message[1:endIdx]
		idx = endIdx + 1 # Should now point to source colon (:).

	# Get the source component (nick and host) of the IRC message.
	# The idx should point to the source part otherwise, it's a PING command.
	if message[idx] == ':':
		idx += 1
		endIdx = message.find(' ', idx)
		source_component = message[idx:endIdx]
		idx = endIdx + 1  # Should point to the command part of the message.

	# Get the command component of the IRC message.
	endIdx = message.find(':', idx)# Looking for the parameters part of the message.
	if -1 == endIdx:                # But not all messages include the parameters part.
		endIdx = len(message)

	command_component = message[idx:endIdx].strip()

	# Get the parameters component of the IRC message.
	if endIdx != len(message):# Check if the IRC message contains a parameters component.
		idx = endIdx + 1            # Should point to the parameters part of the message.
		parameters_component = message[idx:]

	# Parse the command component of the IRC message.
	parsed_message.update({i: x for i, x in parse_command(command_component).items()})

	# Only parse the rest of the components if it's a command
	# we care about we ignore some messages.
	if parsed_message.get('command'):# Is None if it's a message we don't care about.
		if tags_component:# The IRC message contains tags.
			pt = parseTags(tags_component)
			if pt.get('badges'):
				parsed_message['badges'] = pt['badges']
				del pt['badges']
			parsed_message['tags'] = pt

		parsed_message['source'] = parseSource(source_component)

		parsed_message['message'] = parameters_component if parameters_component != '-' else None
		#if rawParametersComponent and rawParametersComponent[0] == '!':  
		#	# The user entered a bot command in the chat window.            
		#	parsed_message['command'] = parseParameters(rawParametersComponent, parsedMessage['command'])

	try:
		return schema.validate(parsed_message)
	except Exception:
		print(traceback.format_exc())
		return parsed_message

# Parses the tags component of the IRC message.
def parseTags(tags):
	# badge-info=badges=broadcaster/1
	#tagsToIgnore = {# List of tags to ignore.
	#	'client-nonce': None,
	#	'flags': None
	#}

	paresed_tags = {}# Holds the parsed list of tags. The key is the tag's name (e.g., color).

	for tag in tags.split(';'):
		split_tags = tag.split('=')  # Tags are key/value pairs.
		value = split_tags[1] if split_tags[1] else None

		match split_tags[0]:# Switch on tag name
			case 'badges':
				# badges=staff/1,broadcaster/1,turbo/1
				if value:
					badge_dict = {}# Holds the list of badge objects. The key is the badge's name (e.g., subscriber).
					for pair in value.split(','):
						badge_parts = pair.split('/')
						badge_dict[badge_parts[0]] = badge_parts[1]
					paresed_tags[split_tags[0]] = badge_dict
				else:
					paresed_tags[split_tags[0]] = None
			case 'badge-info' | 'emotes':
				# emotes=25:0-4,12-16/1902:6-10
				if value:
					emotes_dict = {}# Holds a list of emote objects. The key is the emote's ID.
					for emote in value.split('/'):
						emote_parts = emote.split(':', 1)

						text_positions = []  # The list of position objects that identify the location of the emote in the chat message.
						for position in emote_parts[1].split(','):
							position_parts = position.split('-')
							text_positions.append({
								"start_position": position_parts[0],
								"end_position": position_parts[1]    
							})

						emotes_dict[emote_parts[0]] = text_positions
					paresed_tags[split_tags[0]] = emotes_dict
				else:
					paresed_tags[split_tags[0]] = None
			case 'reply-parent-msg-body':
				paresed_tags[split_tags[0]] = value.replace('\\s', ' ')
			case 'emote-sets':
				# emote-sets=0,33,50,237
				# Array of emote set IDs.
				paresed_tags[split_tags[0]] = value.split(',')
			case _:
				# If the tag is in the list of tags to ignore, ignore
				# it otherwise, add it.
				#if not tagsToIgnore.get(parsedTag[0]):
				paresed_tags[split_tags[0]] = value

	return paresed_tags

# Parses the command component of the IRC message.
def parse_command(command_component):
	parsed_command = None
	command_parts = command_component.split(' ')

	match command_parts[0]:
		case 'JOIN' | 'PART' | 'NOTICE' | 'CLEARCHAT' | 'HOSTTARGET' | 'PRIVMSG':
			parsed_command = {
				"command": command_parts[0],
				"channel": command_parts[1][1:]
			}
		case 'PING':
			parsed_command = {
				"command": command_parts[0]
			}
		case 'CAP':
			parsed_command = {
				"command": command_component,
				# The parameters part of the messages contains the enabled capabilities.
				#"isCapRequestEnabled": True if (command_parts[2] == 'ACK') else False
			}
		case 'GLOBALUSERSTATE':# Included only if you request the /commands capability But it has no meaning without also including the /tags capability.
			parsed_command = {
				"command": command_parts[0]
			}
		# Included only if you request the /commands capability. But it has no meaning without also including the /tags capabilities.
		case 'USERSTATE' | 'ROOMSTATE' | 'USERNOTICE' | 'CLEARMSG':
			parsed_command = {
				"command": command_parts[0],
				"channel": command_parts[1][1:]
			}
		case 'RECONNECT':  
			print('The Twitch IRC server is about to terminate the connection for maintenance.')
			parsed_command = {
				"command": command_parts[0]
			}
		case '421':
			parsed_command = {
				"command": command_parts[0]
			}
			print(f'Unsupported IRC command: {command_parts[2]}')
		# 001 Logged in (successfully authenticated).
		
		# 353 Tells you who else is in the chat room you're joining.
		case '001' | '002' | '003' | '004' | '353' | '366' | '372' | '375' | '376':
			parsed_command = {
				"command": command_parts[0],
				"channel": command_parts[1]
			}
		# Ignoring all other numeric messages.
		#case '002' | '003' | '004' | '353' | '366' | '372' | '375' | '376':
		#	parsed_command = {
		#		"command": command_parts[0],
		#		"channel": command_parts[1][1:]
		#	}
		#	#print(f'numeric message: {commandParts[0]}')
		case _:
			print(f'Unexpected command: {command_parts[0]}')

	return parsed_command

# Parses the source (nick and host) components of the IRC message.
def parseSource(source_component):
	if not source_component:# Not all messages contain a source
		return None
	else:
		source_parts = source_component.split('!')
		return {
			"nick": source_parts[0] if len(source_parts) == 2 else None,
			"host": source_parts[1] if len(source_parts) == 2 else source_parts[0]
		}

# Parsing the IRC parameters component if it contains a command (e.g., !dice).
#def parseParameters(parameters_component, command):
#	idx = 0
#	command_parts = parameters_component[idx + 1:].strip() 
#	params_Idx = command_parts.find(' ')
#	print(command_parts, params_Idx)
#
#	if -1 == params_Idx: # no parameters
#		command['bot_command'] = command_parts[0]
#	else:
#		command['bot_command'] = command_parts[:params_Idx]
#		command['bot_command_params'] = command_parts[params_Idx:].strip()
#		# TODO: remove extra spaces in parameters string
#
#	return command
