from django.test import TestCase
from django.urls import reverse

from .models import Course, ResourceItem, Specialization


class PaginationViewsTests(TestCase):
	def test_resources_page_paginates_specializations(self):
		for index in range(10):
			Specialization.objects.create(
				name=f'Specialization {index}',
				slug=f'specialization-{index}',
			)

		response = self.client.get(reverse('resources'), {'page': 2})

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['specializations'].number, 2)
		self.assertEqual(len(response.context['specializations'].object_list), 2)

	def test_specialization_detail_paginates_courses_and_keeps_filters(self):
		specialization = Specialization.objects.create(name='Radiology', slug='radiology')

		for index in range(11):
			course = Course.objects.create(
				name=f'Course {index}',
				code=f'C{index:02d}',
				academic_year=1,
				semester=1,
			)
			course.specializations.add(specialization)

		response = self.client.get(
			reverse('specialization_detail', args=[specialization.slug]),
			{'year': 1, 'q': 'Course', 'page': 2},
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['courses'].number, 2)
		self.assertEqual(len(response.context['courses'].object_list), 2)
		self.assertIn('year=1', response.context['page_query'])
		self.assertIn('q=Course', response.context['page_query'])
		self.assertNotIn('page=', response.context['page_query'])

	def test_course_detail_paginates_filtered_resources(self):
		course = Course.objects.create(name='Anatomy')

		for index in range(12):
			ResourceItem.objects.create(
				course=course,
				title=f'PDF Resource {index}',
				resource_type='pdf',
				url=f'https://example.com/{index}',
			)

		response = self.client.get(
			reverse('course_detail', args=[course.pk]),
			{'type': 'pdf', 'page': 2},
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['filtered_resources'].number, 2)
		self.assertEqual(len(response.context['filtered_resources'].object_list), 2)
		self.assertIn('type=pdf', response.context['page_query'])
