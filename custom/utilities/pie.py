import decimal

def pi( n:int=2) -> decimal.Decimal:
	"""
	This function calculates the value of pi to 'n' number of places

	Args:
	n:   precision(Decimal places)

	Returns:
	pi:   the value of pi to n-decimal places
	>>> pi(15)
	3.141592653589793
	>>> pi(50)
	3.14159265358979323846264338327950288419716939937510
	>>> pi()
	3.14
	"""
	n = n+2
	m = x = 1

	decimal.getcontext().prec = n + 1
	decimal.getcontext().Emax = 999999999
	c = 426880 * decimal.Decimal(10005).sqrt()
	l = s = decimal.Decimal(13591409)
	for i in range(1, n+1):
		m = decimal.Decimal(m* ((1728*i*i*i)-(2592*i*i)+(1104*i)-120)/(i*i*i))
		l = decimal.Decimal(545140134+l)
		x = decimal.Decimal(-262537412640768000*x)
		s += decimal.Decimal((m*l) / x)
	return decimal.Decimal(f"{c / s}"[:-2])