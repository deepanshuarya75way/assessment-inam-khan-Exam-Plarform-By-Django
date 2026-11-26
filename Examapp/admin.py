from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserRole, Exam, Question, Choice, StudentExam, Answer, PasswordResetOTP, StudentProxy, TeacherProxy, organizations


# ── Student Admin ─────────────────────────────────────────────────────────────

@admin.register(StudentProxy)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_reg_number', 'get_full_name', 'email', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('is_active',)
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login')
    fields = ('username', 'first_name', 'last_name', 'email', 'is_active', 'date_joined', 'last_login')

    def get_queryset(self, request):
        return super().get_queryset(request).filter(userrole__role='student')

    @admin.display(description='Registration Number')
    def get_reg_number(self, obj):
        return obj.username

    @admin.display(description='Full Name')
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or '—'


# ── Teacher Admin ─────────────────────────────────────────────────────────────


@admin.register(TeacherProxy)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('username', 'get_full_name', 'email', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('is_active',)
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login')

    def get_queryset(self, request):
        return super().get_queryset(request).filter(userrole__role='teacher')

    @admin.display(description='Full Name')
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or '—'

    def get_fields(self, request, obj=None):
        if obj is None:
            return ('username', 'first_name', 'last_name', 'email', 'password', 'is_active')
        return ('username', 'first_name', 'last_name', 'email', 'is_active', 'date_joined', 'last_login')

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()
        return ('date_joined', 'last_login')

    def save_model(self, request, obj, form, change):
        if not change:
            raw_password = form.data.get('password')
            if raw_password:
                obj.set_password(raw_password)
        super().save_model(request, obj, form, change)
        UserRole.objects.get_or_create(user=obj, defaults={'role': 'teacher'})


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'duration_minutes', 'total_marks', 'passing_marks', 'is_published', 'start_time', 'end_time')
    list_filter = ('is_published', 'teacher')
    search_fields = ('title', 'teacher__username')
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'exam', 'question_type', 'marks', 'order')
    list_filter = ('question_type', 'exam')
    search_fields = ('question_text',)
    inlines = [ChoiceInline]


@admin.register(StudentExam)
class StudentExamAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'is_submitted', 'obtained_marks', 'tab_switch_count', 'total_suspicion_warnings')
    list_filter = ('is_submitted', 'exam')
    search_fields = ('student__username', 'exam__title')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('student_exam', 'question', 'selected_choice', 'is_correct', 'marks_obtained')
    list_filter = ('is_correct',)


# ── Inline Configuration to show Students inside an Organization ──────────────

from django import forms
from django.forms.models import BaseInlineFormSet

class StudentInlineForm(forms.ModelForm):
    class Meta:
        model = UserRole
        fields = ('user', 'course', 'section')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter the user dropdown selection to only show users with a student role
        self.fields['user'].queryset = User.objects.filter(userrole__role='student')
        
        # 🌟 CRITICAL FIX: Clear the uniqueness validator constraints on this form
        # This prevents Django from throwing "User role with this User already exists"
        if 'user' in self.fields:
            self.fields['user'].validators = []

    def validate_unique(self):
        # 🌟 CRITICAL FIX: Bypass model-level OneToOne uniqueness check during form cleaning
        pass


class StudentInlineFormSet(BaseInlineFormSet):
    def save_new(self, form, commit=True):
        # Handles user rows that are added as fresh values
        user = form.cleaned_data.get('user')
        course = form.cleaned_data.get('course', '')
        section = form.cleaned_data.get('section', '')
        
        user_role, created = UserRole.objects.get_or_create(
            user=user,
            defaults={
                'role': 'student',
                'organization': self.instance,
                'course': course,
                'section': section
            }
        )
        
        if not created:
            user_role.role = 'student'
            user_role.organization = self.instance
            user_role.course = course
            user_role.section = section
            if commit:
                user_role.save()
                
        return user_role

    def save_existing(self, form, instance, commit=True):
        # 🌟 Handles updates to students who are already displayed on this list
        instance.organization = self.instance
        instance.role = 'student'
        if commit:
            instance.save()
        return instance


class StudentInline(admin.TabularInline):
    model = UserRole
    form = StudentInlineForm
    formset = StudentInlineFormSet
    verbose_name = "Enrolled Student"
    verbose_name_plural = "Enrolled Students"
    extra = 1
    fields = ('user', 'course', 'section')

    def get_queryset(self, request):
        return super().get_queryset(request).filter(role='student')


@admin.register(organizations)
class organizationsAdmin(admin.ModelAdmin):
    list_display = ['id', 'org_name']
    search_fields = ('org_name',)
    inlines = [StudentInline]


admin.site.register(Choice)

# Hide the default User section — Students and Teachers have their own sections
admin.site.unregister(User)


@admin.register(PasswordResetOTP)
class PasswordResetOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'created_at', 'is_used')
    list_filter = ('is_used',)
    search_fields = ('user__username',)
    readonly_fields = ('otp', 'created_at')
