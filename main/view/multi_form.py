class FormParser:
    def __init__(self, base_form):
        self.form_base = base_form
        self.form = None

    @staticmethod
    def get_or_create(model, attrs_for_filter):
        try:
            model = model.objects.filter(**attrs_for_filter)[0]
        except IndexError:
            return model.objects.create(**attrs_for_filter)
        return model

    def fill(self, model, attrs_for_filter, disabled) -> None:
        model = FormParser.get_or_create(model=model, attrs_for_filter=attrs_for_filter)
        self.form = self.form_base(instance=model)
        self.form.turn_off(disable=disabled)

    def clear(self, disabled) -> None:
        self.form = self.form_base()
        self.form.turn_off(disable=disabled)

    def post(self, request, model, attrs_for_filter, disabled) -> None:
        model = FormParser.get_or_create(model=model, attrs_for_filter=attrs_for_filter)
        self.form = self.form_base(request, instance=model)
        self.form.turn_off(disable=disabled)

    def __bool__(self):
        return self.form.is_valid()


class Multiform:
    def __init__(self):
        self.model_list = None
        self.models_json = {}

    def get_models_classes(self) -> None:
        # примеры смотрите в коде
        raise NotImplementedError

    def get_post_form(self, disable: bool, request) -> None:
        # вызывать для пост запроса (для изменений данных)
        self.models_json.clear()
        for model in self.model_list:
            form = FormParser(base_form=model['form'])
            form.post(request=request, model=model['form'].Meta.model, attrs_for_filter=model['attrs'], disabled=disable)
            self.models_json.update({str(model['form']()): form})

    def get_fill_form(self, disable) -> None:
        # вызывать для get запроса с учетом заполнения формы из модели
        self.models_json.clear()
        for model in self.model_list:
            form = FormParser(base_form=model['form'])
            form.fill(model=model['form'].Meta.model, attrs_for_filter=model['attrs'], disabled=disable)
            self.models_json.update(
                {str(model['form']()): form})

    def get_clear_form(self, disable) -> None:
        # вызывать для get запроса без заполнения данными из модели (возвращает пустые поля)
        self.models_json.clear()
        for model in self.model_list:
            form = FormParser(base_form=model['form'])
            form.clear(disabled=disable)
            self.models_json.update(
                {str(model['form']()): form})

    def get_form_for_context(self) -> dict:
        # примеры смотрите в коде
        raise NotImplementedError

    def is_valid(self) -> bool:
        # проверяет формы на валидность
        for key, model in self.models_json.items():
            if not model:
                return False
        return True

    def save(self) -> None:
        # сохраняет все формы
        for key, model in self.models_json.items():
            model.form.save()
