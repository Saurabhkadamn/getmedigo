import ast
from pathlib import Path
import unittest


class RouteContractTests(unittest.TestCase):
    def _collect_routes(self, file_path: str) -> set[tuple[str, str]]:
        source = Path(file_path).read_text()
        tree = ast.parse(source)
        routes: set[tuple[str, str]] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                for dec in node.decorator_list:
                    if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute):
                        method = dec.func.attr
                        if method in {"get", "post", "put", "delete", "patch"}:
                            if dec.args and isinstance(dec.args[0], ast.Constant) and isinstance(dec.args[0].value, str):
                                routes.add((method.upper(), dec.args[0].value))
        return routes

    def test_api_gateway_expected_routes(self):
        routes = self._collect_routes("services/api-gateway/app/main.py")
        self.assertIn(("GET", "/health"), routes)
        self.assertIn(("GET", "/ready"), routes)
        self.assertIn(("POST", "/api/v1/auth/login"), routes)
        self.assertIn(("GET", "/api/v1/users/{user_id}"), routes)
        self.assertIn(("GET", "/api/v1/content/home"), routes)

    def test_auth_service_expected_routes(self):
        routes = self._collect_routes("services/auth-service/app/main.py")
        self.assertIn(("GET", "/health"), routes)
        self.assertIn(("GET", "/ready"), routes)
        self.assertIn(("POST", "/auth/login"), routes)

    def test_user_service_expected_routes(self):
        routes = self._collect_routes("services/user-service/app/main.py")
        self.assertIn(("GET", "/health"), routes)
        self.assertIn(("GET", "/ready"), routes)
        self.assertIn(("GET", "/users/{user_id}"), routes)

    def test_content_service_expected_routes(self):
        routes = self._collect_routes("services/content-service/app/main.py")
        self.assertIn(("GET", "/health"), routes)
        self.assertIn(("GET", "/ready"), routes)
        self.assertIn(("GET", "/content/home"), routes)

    def test_gateway_readiness_checks_downstream_services(self):
        source = Path("services/api-gateway/app/main.py").read_text()
        self.assertIn('"auth-service": f"{AUTH_SERVICE_URL}/ready"', source)
        self.assertIn('"user-service": f"{USER_SERVICE_URL}/ready"', source)
        self.assertIn('"content-service": f"{CONTENT_SERVICE_URL}/ready"', source)
        self.assertIn("status_code=503", source)


if __name__ == "__main__":
    unittest.main()
