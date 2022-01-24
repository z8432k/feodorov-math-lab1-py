import numpy as np

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
    colsSum[i] *= rowsGeom[i]
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


def AHPSolve(cw, normVectors, solveVector):
  # Нормированный собственный вектор оценки критериев
  eigVecCalc(cw, eigNormVectors[0])
  awRows, awCols = np.shape(aw)
  # Заполняем нормирпованные собственные вектора оценок альтернатив
  for i in range(awRows):
    eigVecCalc(aw[i], normVectors[i + 1])
  for i in range(awRows):
    solveVector[i] = 0
    for j in range(awCols):
      solveVector[i] += normVectors[0, j] * normVectors[j+1, i]
  minimum = np.amin(solveVector)
  return np.where(solveVector == minimum)






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
awRows, awCols = np.shape(aw)


eigNormVectors = np.zeros([awCols + 1, cwSiz])
ahpSolveVector = np.zeros([awCols])

result1 = AHPSolve(cw, eigNormVectors, ahpSolveVector)

# Матрица нормализации попарных сравнений альтернатив
normPairMatrix = np.zeros([cwSiz, cwSiz, awCols * 2])

normRows, normCols = np.shape(eigNormVectors)
for i in range(normRows):
  if i == 0:
    continue
  for j in range(normRows - 1):
    for k in range(normRows - 1):
      normPairMatrix[i - 1, k, j*2] = eigNormVectors[i, k] / (eigNormVectors[i, k] + eigNormVectors[i, j])
      normPairMatrix[i - 1, k, (j*2+1)] = eigNormVectors[i, j] / (eigNormVectors[i, j] + eigNormVectors[i, k])

ahpPlusSolveMatrix = np.zeros([cwSiz, awCols * 2])
for i in range(cwSiz):
  for j in range(awCols * 2):
    for k in range(cwSiz): # позиция в столбце и счётчик матриц
      ahpPlusSolveMatrix[i, j] += eigNormVectors[0, k] * normPairMatrix[k, i, j]

print(ahpPlusSolveMatrix)



