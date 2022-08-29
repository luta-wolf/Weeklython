from django.contrib import admin

from .models import SchoolObject, Status, ObjectType, Booking, Role, Campus, User


# admin.site.register(SchoolObject)
# admin.site.register(Status)
# admin.site.register(ObjectType)
# admin.site.register(Booking)
# admin.site.register(Role)
# admin.site.register(Campus)
# admin.site.register(User)

@admin.register(SchoolObject)
class SchoolObjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_type_name', 'object_name', 'object_desc', 'get_campus_name', 'object_floor', 'object_room']
    def get_type_name(self, obj):
        return obj.object_type.name
    get_type_name.admin_order_field  = 'object_type'  #Allows column order sorting
    get_type_name.short_description = 'Тип объекта'  #Renames column head
    def get_campus_name(self, obj):
        return obj.object_campus.name
    get_campus_name.admin_order_field  = 'object_campus'  #Allows column order sorting
    get_campus_name.short_description = 'Тип объекта'  #Renames column head
@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_admin']

@admin.register(ObjectType)
class ObjectTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_school_object_name','start','end', 'get_campus_name', 'get_status_name', 'get_user_name',]
    def get_status_name(self, obj):
        return obj.status.name
    get_status_name.admin_order_field  = 'status'  #Allows column order sorting
    get_status_name.short_description = 'Статус'  #Renames column head
    def get_user_name(self, obj):
        return obj.user.login
    get_user_name.admin_order_field  = 'user'  #Allows column order sorting
    get_user_name.short_description = 'Пользователь'  #Renames column head

    def get_start(self, obj):
        pass
    
    def get_school_object_name(self, obj):
        return obj.school_object.object_name
    get_school_object_name.admin_order_field  = 'school_object'  #Allows column order sorting
    get_school_object_name.short_description = 'Объект'  #Renames column head

    def get_campus_name(self, obj):
        return obj.school_object.object_campus.name
    get_campus_name.admin_order_field  = 'school_object.object_campus'  #Allows column order sorting
    get_campus_name.short_description = 'Кампус'  #Renames column head

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'login', 'get_role_name', 'get_campus_name']
    def get_role_name(self, obj):
        return obj.role.name
    get_role_name.admin_order_field  = 'role'  #Allows column order sorting
    get_role_name.short_description = 'Статус'  #Renames column head
    
    def get_campus_name(self, obj):
        return obj.campus.name
    get_campus_name.admin_order_field  = 'campus'  #Allows column order sorting
    get_campus_name.short_description = 'Кампус'  #Renames column head

    