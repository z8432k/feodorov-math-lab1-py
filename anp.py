import numpy as np

cw = np.array([ 3, 7, 5, 1, 9 ])
cwSiz = len(cw);

# Оценки по критериям уложены по строкам
aw = np.array([
  [3, 1, 5, 4, 9], # Оценка альтернативы а1 по критериям с1-с5
  [1, 2, 6, 9, 1], # Оценка альтернативы а2 по критериям с1-с5
  [8, 5, 9, 7, 6], # ...
  [4, 8, 7, 8, 5],
  [5, 9, 2, 5, 3]
])

def geo_mean(iterable):
    a = np.array(iterable)
    return a.prod()**(1.0/len(a))

def eigenVec(m):
  rows, cols = m.shape
  rowsGeom = np.ones([cols])
  for i in range(rows):
    row = m[i]
    geom = geo_mean(row)
    rowsGeom[i] = geom
  geomSum = np.sum(rowsGeom)
  for i in range(rows):
    rowsGeom[i] = rowsGeom[i] / geomSum
  # lambda
  colsSum = np.zeros([rows])
  for i in range(rows):
    for k in range(cols):
      colsSum[i] += m[k, i]
    colsSum[i] *= rowsGeom[i];
  lmbda = np.sum(colsSum)
  if (lmbda > rows):
    raise "Wrong lambda"
  return rowsGeom


# Считаем Относительные оценки критериев
critRelEv = np.ones([cwSiz, cwSiz])
for i in range(cwSiz):
  for k in range(cwSiz):
    result = cw[i] / cw[k]
    critRelEv[i,k] = result
critEig = eigenVec(critRelEv)
print(critEig)


