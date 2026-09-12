"""Lunar Drift Wallpaper Service - Android bridge"""
try:
    from jnius import autoclass, PythonJavaClass, java_method
except ImportError:
    autoclass = None
    PythonJavaClass = object

if autoclass:
    WallpaperService = autoclass('android.service.wallpaper.WallpaperService')
    class LunarDriftWallpaperService(PythonJavaClass):
        __javainterfaces__ = ('android/service/wallpaper/WallpaperService',)
        __javaclass__ = 'org/lunardrift/lunardrift/LunarDriftWallpaperService'
        def __init__(self):
            super().__init__()
        @java_method('(Landroid/view/SurfaceHolder;)Landroid/service/wallpaper/WallpaperService$Engine;')
        def onCreateEngine(self, holder):
            return None
else:
    class LunarDriftWallpaperService:
        pass
