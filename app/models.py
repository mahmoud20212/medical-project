import random
from django.db import models
from django.templatetags.static import static


ICON_CHOICES = (
	('school', 'مدرسة'),
	('radiology', 'الأشعات'),
	('body_system', 'الجسم'),
	('biotech', 'التكنولوجيا الحيوية'),
	('microbiology', 'الميكروبيولوجي'),
	('clinical_notes', 'الملاحظات الإكلينيكية'),
	('medical_services', 'الخدمات الطبية'),
	('psychology', 'علم النفس'),
	('skeleton', 'الهيكل العظمي'),
	('lab_panel', 'لوحة المختبر'),
	('science', 'العلوم'),
	('health_and_safety', 'الصحة والسلامة'),
	('medication', 'الأدوية'),
	('vaccines', 'اللقاحات'),
	('monitor_heart', 'مراقبة القلب'),
	('ecg_heart', 'تخطيط القلب'),
	('bloodtype', 'فصائل الدم'),
	('healing', 'العلاج'),
	('emergency', 'الطوارئ'),
	('local_hospital', 'المستشفى'),
	('stethoscope', 'السماعة الطبية'),
	('heart_broken', 'أمراض القلب'),
	('neurology', 'الأعصاب'),
	('pulmonology', 'الجهاز التنفسي'),
	('ophthalmology', 'طب العيون'),
	('dentistry', 'طب الأسنان'),
	('pediatrics', 'طب الأطفال'),
	('elderly', 'طب الشيخوخة'),
	('pregnant_woman', 'النساء والولادة'),
	('female', 'صحة المرأة'),
	('male', 'صحة الرجل'),
	('accessible', 'العلاج الطبيعي'),
	('fitness_center', 'اللياقة والتأهيل'),
	('monitor_weight', 'الوزن والتغذية'),
	('nutrition', 'التغذية'),
	('coronavirus', 'الأمراض المعدية'),
	('sanitizer', 'التعقيم'),
	('masks', 'الوقاية'),
	('experiment', 'التجارب'),
	('genetics', 'الوراثة'),
	('vaccines', 'التطعيم'),
	('syringe', 'الحقن'),
	('pill', 'الحبوب الطبية'),
	('medical_information', 'المعلومات الطبية'),
	('patient_list', 'المرضى'),
	('ambulance', 'الإسعاف'),
	('lab_research', 'الأبحاث المخبرية'),
	('orthopedics', 'العظام'),
	('dermatology', 'الجلدية'),
	('urology', 'المسالك البولية'),
	('psychiatry', 'الطب النفسي'),
	('medical_mask', 'الكمامات'),
	('wheelchair_pickup', 'الكراسي المتحركة'),
	('hearing', 'السمع'),
	('visibility', 'البصر'),
	('handshake', 'الرعاية الصحية'),
	('self_improvement', 'الصحة النفسية'),
	# general icons
  ('quiz', 'الاختبارات'),
	('assignment', 'الواجبات'),
	('link', 'الروابط'),
	('menu_book', 'المراجع'),
	('video_library', 'الفيديوهات'),
	('article', 'المقالات'),
	('description', 'الملفات'),
	('folder', 'المجلدات'),
	('image', 'الصور'),
	('smart_display', 'العروض'),
	('record_voice_over', 'المحاضرات'),
	('live_help', 'الأسئلة الشائعة'),
	('forum', 'النقاشات'),
	('chat', 'الدردشة'),
	('groups', 'المجموعات'),
	('person', 'الطلاب'),
	('supervisor_account', 'المشرفين'),
	('notifications', 'الإشعارات'),
	('event', 'الأحداث'),
	('calendar_month', 'التقويم'),
	('timeline', 'التقدم'),
	('insights', 'الإحصائيات'),
	('analytics', 'التحليلات'),
	('dashboard', 'لوحة التحكم'),
	('settings', 'الإعدادات'),
	('admin_panel_settings', 'الإدارة'),
	('search', 'البحث'),
	('bookmark', 'المحفوظات'),
	('favorite', 'المفضلة'),
	('download', 'التحميلات'),
	('upload', 'الرفع'),
	('cloud', 'السحابة'),
	('security', 'الأمان'),
	('lock', 'الخصوصية'),
	('support', 'الدعم'),
	('email', 'البريد'),
	('language', 'المواقع'),
	('public', 'الإنترنت'),
)

class Specialization(models.Model):
	name = models.CharField(max_length=120, verbose_name='الاسم')
	description = models.TextField(blank=True, null=True, verbose_name='الوصف')
	slug = models.SlugField(unique=True, verbose_name='الرابط المختصر')
	image_url = models.URLField(blank=True, null=True, verbose_name='رابط الصورة')
	icon = models.CharField(
		max_length=50,
		choices=ICON_CHOICES,
		default='school',
		verbose_name='الأيقونة',
	)
	display_order = models.PositiveSmallIntegerField(default=1, verbose_name='ترتيب العرض')
	is_active = models.BooleanField(default=True, verbose_name='مفعل')

	class Meta:
		ordering = ['display_order', 'name']
		verbose_name = 'تخصص'
		verbose_name_plural = 'التخصصات'

	def __str__(self) -> str:
		return self.name

	@property
	def get_image_url(self) -> str:
		if not self.image_url:
			random_number = random.randint(1, 8)
			return static(f'images/{random_number}.png')
		return self.image_url

class Course(models.Model):
	YEAR_CHOICES = (
		(1, 'السنة الأولى'),
		(2, 'السنة الثانية'),
		(3, 'السنة الثالثة'),
		(4, 'السنة الرابعة'),
	)
	SEMESTER_CHOICES = (
		(1, 'الفصل الأول'),
		(2, 'الفصل الثاني'),
	)
	LEVEL_CHOICES = (
		('basic', 'أساسي'),
		('intermediate', 'متوسط'),
		('advanced', 'متقدم'),
		('privilege', 'امتياز'),
	)
	
	academic_year = models.PositiveSmallIntegerField(
		choices=YEAR_CHOICES,
		verbose_name='السنة الدراسية',
		null=True,
		blank=True,
  )
	semester = models.PositiveSmallIntegerField(
		choices=SEMESTER_CHOICES,
		verbose_name='الفصل الدراسي',
		null=True,
		blank=True,
  )
	icon = models.CharField(
		max_length=50,
		choices=ICON_CHOICES,
		default='school',
		verbose_name='الأيقونة',
	)
	code = models.CharField(max_length=20, blank=True, null=True, verbose_name='رمز المقرر')
	name = models.CharField(max_length=120, verbose_name='اسم المقرر')
	description = models.TextField(blank=True, verbose_name='الوصف')
	specializations = models.ManyToManyField(
		Specialization,
		related_name='courses',
		verbose_name='التخصصات',
		blank=True,
  )
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
	updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

	class Meta:
		ordering = ['code']
		verbose_name = 'المقرر'
		verbose_name_plural = 'المقررات'

	def __str__(self) -> str:
		return f'{self.name}'

class ResourceItem(models.Model):
	RESOURCE_TYPE_CHOICES = (
		('pdf', 'PDF'),
		('slides', 'سلايدات'),
		('lecture', 'محاضرة'),
		('video', 'فيديو'),
		('summary', 'ملخص'),
		('exam', 'اختبار'),
		('link', 'رابط'),
	)

	course = models.ForeignKey(
		Course,
		on_delete=models.CASCADE,
		related_name='resources',
		verbose_name='المقرر',
	)
	title = models.CharField(max_length=180, verbose_name='العنوان')
	resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES, verbose_name='نوع المورد')
	url = models.URLField(blank=True, verbose_name='الرابط')
	description = models.CharField(max_length=255, blank=True, verbose_name='الوصف')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
	updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

	class Meta:
		ordering = ['title']
		verbose_name = 'مورد'
		verbose_name_plural = 'الموارد'
		# get_latest_by = 'updated_at'

	def __str__(self) -> str:
		return self.title


class SiteSettings(models.Model):
	site_name = models.CharField(max_length=180, default='كلية العلوم الطبية التطبيقية', verbose_name='اسم الموقع')
	site_tagline = models.CharField(max_length=220, blank=True, verbose_name='الوصف المختصر')
	show_specializations = models.BooleanField(default=True, verbose_name='إظهار التخصصات في الرئيسية')
	show_team = models.BooleanField(default=True, verbose_name='إظهار فريق العمل في الرئيسية')
	updated_at = models.DateTimeField(auto_now=True, verbose_name='آخر تحديث')

	class Meta:
		verbose_name = 'إعدادات الموقع'
		verbose_name_plural = 'إعدادات الموقع'

	def save(self, *args, **kwargs):
		self.pk = 1
		super().save(*args, **kwargs)

	def __str__(self) -> str:
		return 'إعدادات الموقع'


class HomePageContent(models.Model):
	badge_text = models.CharField(max_length=100, default='التميز الأكاديمي', verbose_name='نص الوسم')
	hero_title = models.CharField(max_length=255, verbose_name='عنوان الواجهة الرئيسية', default='مصادر دراسية لطلاب كلية العلوم الطبية التطبيقية')
	hero_description = models.TextField(verbose_name='وصف الواجهة الرئيسية', default='اكتشف مجموعة شاملة من الموارد الدراسية المصممة خصيصًا لطلاب كلية العلوم الطبية التطبيقية. من المقررات الدراسية إلى الاختبارات والمحاضرات، كل ما تحتاجه لتحقيق التفوق الأكاديمي في مكان واحد.')
	primary_button_text = models.CharField(max_length=80, default='استكشف المصادر', verbose_name='نص الزر ')
	primary_button_url = models.CharField(max_length=255, default='#', verbose_name='رابط الزر')
	hero_background_image_url = models.URLField(blank=True, verbose_name='رابط صورة الخلفية')
	primary_logo_url = models.URLField(blank=True, verbose_name='رابط الشعار الأساسي')
	secondary_logo_url = models.URLField(blank=True, verbose_name='رابط الشعار الثانوي')
	updated_at = models.DateTimeField(auto_now=True, verbose_name='آخر تحديث')

	class Meta:
		verbose_name = 'محتوى الصفحة الرئيسية'
		verbose_name_plural = 'محتوى الصفحة الرئيسية'
  
	@property
	def get_hero_background_image_url(self) -> str:
		if not self.hero_background_image_url:
			random_number = random.randint(1, 8)
			return static(f'images/{random_number}.png')
		return self.hero_background_image_url

	def save(self, *args, **kwargs):
		self.pk = 1
		super().save(*args, **kwargs)

	def __str__(self) -> str:
		return 'محتوى الصفحة الرئيسية'


class Team(models.Model):
	name = models.CharField(max_length=150, verbose_name='الاسم')
	job_title = models.CharField(max_length=180, verbose_name='المسمى الوظيفي')
	bio = models.TextField(blank=True, verbose_name='نبذة')
	image_url = models.URLField(blank=True, verbose_name='رابط الصورة')
	display_order = models.PositiveSmallIntegerField(default=1, verbose_name='ترتيب العرض')
	is_active = models.BooleanField(default=True, verbose_name='مفعل')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
	updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

	class Meta:
		ordering = ['display_order', 'name']
		verbose_name = 'عضو فريق'
		verbose_name_plural = 'فريق العمل'
  
	@property
	def get_image_url(self) -> str:
		if not self.image_url:
			return static(f'images/user.png')
		return self.image_url

	def __str__(self) -> str:
		return self.name

