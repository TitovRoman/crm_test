from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.shortcuts import redirect


class MyPassesTestMixin(AccessMixin):
    def test_func(self, request, *args, **kwargs):
        raise NotImplementedError(
            '{0} is missing the implementation of the test_func() method.'
            .format(self.__class__.__name__)
        )

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.test_func(request, *args, **kwargs)
        if not user_test_result:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)


class _CheckModelEmployeeOrAdministratorMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            employee = self.model.objects.get(pk=kwargs['pk']).employee
        except:
            return redirect(self.redirect_url)
        if employee != request.user and not request.user.is_administrator:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)


class AdministratorMixin(LoginRequiredMixin, MyPassesTestMixin):
    def test_func(self, request, *args, **kwargs):
        return request.user.is_administrator


class EmployeeMixin(LoginRequiredMixin, MyPassesTestMixin):
    def test_func(self, request, *args, **kwargs):
        return request.user.is_employee


class AdministratorOrEmployeeMixin(LoginRequiredMixin, MyPassesTestMixin):
    def test_func(self, request, *args, **kwargs):
        return request.user.is_employee or request.user.is_administrator


class AdministratorOrModelEmployeeMixin(
    LoginRequiredMixin,
    _CheckModelEmployeeOrAdministratorMixin,
):
    pass
