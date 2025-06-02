import numpy as np
import matplotlib.ticker as ticker
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from typing import Optional, List

def make_space_fig(ax, title: str, box: Optional[List[float]] = None):
    """
    设置地图子图 (ax) 的刻度、格式和标题，并返回修改后的 ax。

    输入:
        ax: cartopy/matplotlib 的子图对象 (Axes)。
        title (str): 子图标题。
        box (Optional[List[float]]): 可选，地图的经纬度范围 [lon_min, lon_max, lat_min, lat_max]。
                                      如果未提供，默认使用 [0, 360, -20, 20]。

    输出:
        ax: 返回设置好的子图对象。

    示例:
        fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
        makefig(ax, title='Example Map', box=[0, 360, -30, 30])
        plt.show()
    """
    if box is None:
        box = [0, 360, -20, 20]
    
    # 设置经纬度刻度
    ax.set_xticks(np.linspace(box[0], box[1], 7), crs=ccrs.PlateCarree())
    ax.set_yticks(np.linspace(box[2], box[3], 5), crs=ccrs.PlateCarree())

    # 设置格式
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())

    # 设置主刻度和副刻度
    ax.xaxis.set_major_locator(ticker.MultipleLocator((box[1] - box[0]) / 6))
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(6))
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(5))

    # 标题和刻度样式
    ax.set_title(title, loc='left')
    ax.tick_params(which='major', length=5)

    return ax


def plot_space_data(
    data,
    ax,
    cmap,
    fmt: str,
    title: str,
    box: Optional[List[float]] = None,
    levels: Optional[np.ndarray] = None
):
    """
    在给定的子图 (ax) 上绘制等值填色图 (contourf)，并进行地图美化设置。

    输入:
        data: 待绘制的 xarray.DataArray 或类似对象，通常是二维地理数据。
        ax: matplotlib/cartopy 的子图对象 (Axes)。
        cmap: matplotlib 颜色映射 (Colormap)。
        fmt (str): 数据单位或说明，将用于 colorbar 标注或图示说明。
        title (str): 子图标题。
        box (Optional[List[float]]): 地图显示范围 [lon_min, lon_max, lat_min, lat_max]，默认 [0, 360, -20, 20]。
        levels (Optional[np.ndarray]): 等值线的划分等级，默认是 np.linspace(0, 4, 41)。

    输出:
        f: 返回绘制的 contourf 图层对象 (QuadContourSet)。

    示例:
        fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
        plot_data(data, ax, cmap='viridis', fmt='mm/day', title='Rainfall', box=[0, 360, -30, 30])
        plt.show()
    """
    if box is None:
        box = [0, 360, -20, 20]
    
    if levels is None:
        levels = np.linspace(0., 4., 41)
    
    # 绘制填色图
    f = data.plot.contourf(
        ax=ax,
        cmap=cmap,
        add_labels=False,
        levels=levels,
        add_colorbar=False,
        transform=ccrs.PlateCarree()
    )

    # 地图基本设置
    ax.coastlines()
    ax.set_extent(box, crs=ccrs.PlateCarree())
    ax.set_aspect(3)
    
    # 调用辅助函数设置标题与刻度（需存在 makefig 函数）
    make_space_fig(ax, title, box)
    
    # 美化子图边框
    for spine in ax.spines.values():
        spine.set_linewidth(1.1)

    return f
