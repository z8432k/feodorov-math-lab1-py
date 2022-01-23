import numpy as np

cw = np.array([ 3, 7, 5, 1, 9 ])
cwSiz = len(cw);

# Оценки по критериям уложены по строкам
aw = np.array([
  [3, 1, 8, 4, 5],
  [1, 2, 5, 8, 9],
  [5, 6, 9, 7, 2],
  [4, 9, 7, 8, 5],
  [9, 1, 6, 5, 3]
])

def geo_mean(iterable):
    a = np.array(iterable)
    return a.prod()**(1.0/len(a))


def eigenVec(m, dst=None):
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
  if (not dst is None):
    np.copyto(dst, rowsGeom)
  return rowsGeom

def eigVecCalc(srcVec, dstVec):
  srcSiz = len(srcVec)
  result = np.ones([srcSiz, srcSiz])
  for i in range(srcSiz):
    for k in range(srcSiz):
      result[i, k] = srcVec[i] / srcVec[k]
  eigenVec(result, dstVec)




eigVectors = np.zeros([cwSiz + 1, cwSiz]);

# Нормированный собственный вектор оценки критериев
eigVecCalc(cw, eigVectors[0])

# Заполняем нормирпованные собственные вектора оценок альтернатив
awRows, awCols = np.shape(aw)
for i in range(awRows):
  eigVecCalc(aw[i], eigVectors[i + 1])


print(eigVectors)

