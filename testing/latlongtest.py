import pyproj

inProj = pyproj.Proj('epsg:32119')
outProj = pyproj.Proj('epsg:4326')

print(inProj)

x1, y1 = 640078.8989077978, 225551.9748539497

transformer = pyproj.Transformer.from_proj(inProj, 'epsg:4326')
x2, y2 = transformer.transform(x1, y1)

print(x2, y2)
