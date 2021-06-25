import xadmin
from users.models import VerifyCode
from xadmin import views


class BaseSetting(object):
    # 添加主题功能
    enable_themes = True
    user_bootswatch = True


class GlobalSettings(object):
    # 全局配置，后端管理标题和页脚
    site_title = '天天生鲜后台管理'
    site_footer = 'https://www.qnmlgb.top/'
    # 菜单收缩
    menu_style = 'accordion'


class VerifyCodeAdmin(object):
    list_display = ['code', 'mobile', 'add_time']


xadmin.site.register(VerifyCode, VerifyCodeAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
