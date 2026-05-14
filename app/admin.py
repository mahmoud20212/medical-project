from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.utils.html import format_html

from .models import (
	Course,
	HomePageContent,
	ICON_CHOICES,
	ResourceItem,
	SiteSettings,
	Specialization,
	Team,
)

# Unregister User and Group models
admin.site.unregister(User)
admin.site.unregister(Group)

ADMIN_MEDIA_CSS = (
	'app/admin_specialization.css',
	'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0',
)
ADMIN_MEDIA_JS = ('app/admin_icons.js',)


class IconMediaMixin:
	class Media:
		css = {'all': ADMIN_MEDIA_CSS}
		js = ADMIN_MEDIA_JS

class IconRadioSelect(forms.RadioSelect):
	def render(self, name, value, attrs=None, renderer=None):
		value = '' if value is None else str(value)
		attrs = {} if attrs is None else attrs.copy()

		base_id = attrs.get('id', '')
		html_items = []

		for index, (option_value, option_label) in enumerate(self.choices):
			option_value = str(option_value)
			input_id = f'{base_id}_{index}' if base_id else f'id_{index}'

			checked = ' checked' if value == option_value else ''

			html = (
				f'<label class="icon-radio-option">'
				f'<input type="radio" name="{name}" value="{option_value}" id="{input_id}"{checked}>'
				f'<span class="icon-radio-card">'
				f'<span class="material-symbols-outlined icon-radio-symbol">{option_value}</span>'
				f'<span class="icon-radio-label">{option_label}</span>'
				f'</span>'
				f'</label>'
			)
			html_items.append(html)

		return format_html(
			'<div class="icon-radio-grid">{}</div>',
			format_html(''.join(html_items))
		)

class IconAdminForm(forms.ModelForm):
	icon = forms.ChoiceField(
		choices=ICON_CHOICES,
		widget=IconRadioSelect,
		label='الأيقونة',
	)


class SpecializationAdminForm(IconAdminForm):
	class Meta:
		model = Specialization
		fields = '__all__'


class CourseAdminForm(IconAdminForm):
	class Meta:
		model = Course
		fields = '__all__'


class IconPreviewAdminMixin:
	@admin.display(description='معاينة')
	def icon_preview(self, obj):
		icon_name = getattr(obj, 'icon', '') or 'school'
		return format_html(
			'<span style="display:inline-flex;align-items:center;gap:8px;">'
			'<span class="material-symbols-outlined" style="font-size:24px;line-height:1;">{}</span>'
			'<span>{}</span>'
			'</span>',
			icon_name,
			icon_name,
		)

class ResourceItemInline(admin.TabularInline):
	"""عرض الموارد داخل صفحة المقرر"""
	model = ResourceItem
	extra = 1
	fields = ('title', 'resource_type', 'url', 'description')
	ordering = ('title',)

@admin.register(Specialization)
class SpecializationAdmin(IconMediaMixin, IconPreviewAdminMixin, admin.ModelAdmin):

	form = SpecializationAdminForm
	list_display = ('name', 'icon_preview', 'slug', 'display_order', 'is_active')
	list_filter = ('is_active',)
	search_fields = ('name', 'slug')
	ordering = ('display_order', 'name')
	prepopulated_fields = {'slug': ('name',)}
	fieldsets = (
		('البيانات الأساسية', {
			'fields': ('name', 'slug', 'is_active', 'description')
		}),
		('الترتيب', {
			'fields': ('display_order',)
		}),
		('التصميم', {
			'fields': ('image_url', 'icon', 'icon_preview')
		}),
	)
	readonly_fields = ('icon_preview',)


@admin.register(Course)
class CourseAdmin(IconMediaMixin, IconPreviewAdminMixin, admin.ModelAdmin):

	form = CourseAdminForm
	list_display = ('name', 'code', 'academic_year', 'semester', 'resources_count', 'specializations_list', 'icon_preview')
	list_filter = ('academic_year', 'semester', 'specializations')
	search_fields = ('code', 'name')
	ordering = ('code',)
	filter_horizontal = ('specializations',)
	fieldsets = (
		('المعلومات الأساسية', {
			'fields': ('name', 'code', 'description')
		}),
		('التصنيف الدراسي', {
			'fields': ('academic_year', 'semester', 'specializations')
		}),
		('التصميم', {
			'fields': ('icon', 'icon_preview')
		}),
	)
	readonly_fields = ('icon_preview',)
	inlines = [ResourceItemInline]

	@admin.display(description='الموارد')
	def resources_count(self, obj):
		count = obj.resources.count()
		return format_html(
			'<span style="background:#6aa84f;color:white;padding:3px 8px;border-radius:3px;">{}</span>',
			count
		)

	@admin.display(description='التخصصات')
	def specializations_list(self, obj):
		names = list(obj.specializations.values_list('name', flat=True))
		return '، '.join(names) if names else '-'


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
	list_display = ('site_name', 'updated_at')
	readonly_fields = ('updated_at',)


@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
	list_display = ('hero_title', 'badge_text', 'updated_at')
	readonly_fields = ('updated_at',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
	list_display = ('name', 'job_title', 'display_order', 'is_active', 'updated_at')
	list_filter = ('is_active',)
	search_fields = ('name', 'job_title')
	ordering = ('display_order', 'name')
	fieldsets = (
		('البيانات الأساسية', {
			'fields': ('name', 'job_title', 'bio')
		}),
		('التصميم', {
			'fields': ('image_url',)
		}),
		('التحكم', {
			'fields': ('display_order', 'is_active', 'updated_at')
		}),
	)
	readonly_fields = ('updated_at',)