import scipy.stats as st

rv = st.poisson(10)

print (rv.pmf(3))