import os
import rasterio

from rasterio.warp import calculate_default_transform, reproject, Resampling

def reprojection(srcPath, dst_crs):
    """
    Majorly for multiple rasters reprojection, although it can also be used for one raster.
    Parameter:
    srcPath: folder path to the raster to be projected.
    dst_crs: desired CRS e.g. dst = 'EPSG:26332'.
    """
    
    rasterfiles = [i for i in os.listdir(srcPath) if i.endswith('tif')]
    for src in rasterfiles:
        dst = src[:-4]+'_prj'+src[-4:]
        #input raster
        src = rasterio.open(srcPath+src)

        #tranformation
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds)

        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })
        dstPath = srcPath+"/reprojected/"
        isExist = os.path.exists(dstPath)
        if not isExist:
            os.makedirs(dstPath)
        dst = rasterio.open(dstPath+dst, 'w', **kwargs)
        #write output dataset
        for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest)
        dst.close()
