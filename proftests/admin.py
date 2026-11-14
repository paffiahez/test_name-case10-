from django.contrib import admin

from .models import AnswerOption, AnswerOptionScore, Question, StudyDirection, Test


class AnswerOptionScoreInline(admin.TabularInline):
    model = AnswerOptionScore
    extra = 1


class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 2
    show_change_link = True


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'test', 'order')
    list_filter = ('test',)
    inlines = [AnswerOptionInline]


@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question')
    inlines = [AnswerOptionScoreInline]


admin.site.register(StudyDirection)
