from django.apps import AppConfig

class BoardsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_board.boards'

    def ready(self):
        # ここでカスタムコマンドを登録
        try:
            import boards.commands
        except ImportError:
            pass
