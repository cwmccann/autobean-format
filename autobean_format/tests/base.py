import io
from typing import Optional, Type
from autobean_refactor import models, parser as parser_lib
from autobean_format import formatter, options_lib
import pytest


_DEFAULT_OPTIONS = options_lib.Options(
    indent='    ',
    currency_column=80,
    output_mode=options_lib.OutputMode.STDOUT,
    recursive=False,
)


class BaseTest:
    @pytest.fixture(autouse=True)
    def _setup_parser(self, parser: parser_lib.Parser) -> None:
        self.parser = parser

    def _format(self, model: models.RawModel, options: options_lib.Options) -> str:
        stream = io.StringIO()
        formatter.format(model, options, stream)
        return stream.getvalue()

    def format(
        self,
        text: str,
        model_type: Type[models.RawTreeModel],
        options: Optional[options_lib.Options] = None,
    ) -> str:
        model = self.parser.parse(text, model_type)
        model.auto_claim_comments()
        return self._format(model, options or _DEFAULT_OPTIONS)

    def format_token(
        self,
        text: str,
        model_type: Type[models.RawTokenModel],
        options: Optional[options_lib.Options] = None,
    ) -> str:
        model = self.parser.parse_token(text, model_type)
        return self._format(model, options or _DEFAULT_OPTIONS)
