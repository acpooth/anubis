#!/usr/bin/env python3

### Scritp for testing plots



###########################
# Pureba para bubble plot #
###########################

# datos de prueba
n = 20
m = 25
X = np.random.randint(6, size=(n, m))
rows_ = ['r_'+str(i) for i in range(1, n+1)]
cols_ = ['c_'+str(i) for i in range(1, m+1)]

df = pd.DataFrame(X, columns=cols_, index=rows_)

# END datos de prueba
