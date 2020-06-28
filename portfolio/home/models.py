from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, TabbedInterface, ObjectList, RichTextFieldPanel, \
    StreamFieldPanel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel


@register_setting(icon='placeholder')
class PortfolioSettings(BaseSetting):

    seo_keywords = models.CharField(
        verbose_name=_('Mots clés SEO'),
        max_length=256,
        blank=True,
        default='',
    )
    seo_description = models.CharField(
        verbose_name=_('Description SEO'),
        max_length=512,
        blank=True,
        default='',
    )

    google_analytics_id = models.CharField(
        verbose_name=_('Google Analytics ID'),
        max_length=128,
        blank=True,
        default='',
    )

    twitter_url = models.URLField(blank=True, default='')
    facebook_url = models.URLField(blank=True, default='')
    linkedin_url = models.URLField(blank=True, default='')

    seo_panels = [
        FieldPanel('seo_keywords'),
        FieldPanel('seo_description'),
        MultiFieldPanel(
            [
                FieldPanel('google_analytics_id'),
            ],
            heading=_('Google Analytics'),
        ),
    ]
    social_panels = [
        FieldPanel('twitter_url'),
        FieldPanel('facebook_url'),
        FieldPanel('linkedin_url'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(seo_panels, heading=_('SEO')),
        ObjectList(social_panels, heading=_('Réseaux sociaux')),
    ])

    class Meta:
        db_table = 'portfolio_settings'
        verbose_name = 'Portfolio'


class ServiceBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=128)
    text = blocks.TextBlock()
    icon = blocks.CharBlock(max_length=128)

    class Meta:
        template = 'home/blocks/service.html'
        icon = 'time'


class SkillBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=128)
    subheading = blocks.CharBlock(
        max_length=128,
        required=False,
        help_text=_('Sous-titre dans la vue grille'),
    )
    intro = blocks.CharBlock(
        max_length=255,
        required=False,
        help_text=_('Sous-titre dans la vue modal (grand écran)'),
    )
    image = ImageChooserBlock()
    text = blocks.TextBlock(required=False)

    class Meta:
        template = 'home/blocks/skill.html'
        icon = 'code'


class ExperienceBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=128)
    date = blocks.CharBlock(max_length=128)
    subheading = blocks.CharBlock(max_length=128, required=False)
    text = blocks.TextBlock(required=False)
    image = ImageChooserBlock()

    class Meta:
        template = 'home/blocks/experience.html'
        icon = 'date'


class HomePage(Page):

    # Header
    header_lead = models.CharField(
        verbose_name=_('Slogan'),
        max_length=255,
        blank=True,
        default='',
    )
    header_heading = models.CharField(
        verbose_name=_('Titre'),
        max_length=128,
        default='',
    )
    header_slide = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Slide'),
        related_name='+',
    )

    # About
    biography_heading = models.CharField(
        verbose_name=_('Titre'),
        max_length=128,
        default='',
    )
    biography_subheading = models.CharField(
        verbose_name=_('Sous-titre'),
        max_length=128,
        blank=True,
        default='',
    )
    biography_text = RichTextField(blank=True)

    # Services
    service_subheading = models.CharField(
        verbose_name=_('Sous-titre'),
        max_length=255,
        blank=True,
        default='',
    )
    services = StreamField(
        [('service', ServiceBlock())],
        null=True,
        blank=True,
    )

    # Skills
    skill_heading = models.CharField(
        verbose_name=_('Titre'),
        max_length=255,
        blank=True,
        default='',
    )
    skill_subheading = models.CharField(
        verbose_name=_('Sous-titre'),
        max_length=255,
        blank=True,
        default='',
    )
    skills = StreamField(
        [('skill', SkillBlock())],
        null=True,
        blank=True,
    )

    # Experiences
    experience_heading = models.CharField(
        verbose_name=_('Titre'),
        max_length=255,
        blank=True,
        default='',
    )
    experience_subheading = models.CharField(
        verbose_name=_('Sous-titre'),
        max_length=255,
        blank=True,
        default='',
    )
    experiences = StreamField(
        [('experience', ExperienceBlock())],
        null=True,
        blank=True,
    )

    # Contact
    contact_address = models.CharField(max_length=255, blank=True, default='')
    contact_email = models.EmailField(blank=True, default='')
    contact_phone = models.CharField(max_length=128, blank=True, default='')

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('header_lead'),
                FieldPanel('header_heading'),
                ImageChooserPanel('header_slide'),
            ],
            heading=_('Entête'),
        ),
        MultiFieldPanel(
            [
                FieldPanel('biography_heading'),
                FieldPanel('biography_subheading'),
                RichTextFieldPanel('biography_text'),
            ],
            heading=_('Biographie'),
        ),
        MultiFieldPanel(
            [
                FieldPanel('service_subheading'),
                StreamFieldPanel('services'),
            ],
            heading=_('Services'),
        ),
        MultiFieldPanel(
            [
                FieldPanel('skill_heading'),
                FieldPanel('skill_subheading'),
                StreamFieldPanel('skills'),
            ],
            heading=_('Compétences'),
        ),
        MultiFieldPanel(
            [
                FieldPanel('experience_heading'),
                FieldPanel('experience_subheading'),
                StreamFieldPanel('experiences'),
            ],
            heading=_('Mon parcours'),
        ),
        MultiFieldPanel(
            [
                FieldPanel('contact_address'),
                FieldPanel('contact_email'),
                FieldPanel('contact_phone'),
            ],
            heading=_('Contact'),
        ),
    ]

    class Meta:
        db_table = 'portfolio_homepage'
        verbose_name = _("Page d'accueil")
