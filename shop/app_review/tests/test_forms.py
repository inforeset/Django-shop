from django.test import TestCase
from django.forms import Textarea
from app_review.forms import ReviewForm


class ReviewFormFormTest(TestCase):

    def test_field_text_form(self):
        form = ReviewForm()
        self.assertEqual(form.fields['text'].max_length, 300)
        self.assertTrue(form.fields['text'].required)
        self.assertTrue(form.fields['text'].widget.__class__.__name__ == Textarea().__class__.__name__)