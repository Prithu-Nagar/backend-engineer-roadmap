"""Flask API for creating and inspecting notification requests."""

from __future__ import annotations

from uuid import uuid4

from flask import Flask, jsonify, request
from providers import LocalNotificationProvider
from service import (
    IdempotencyConflictError,
    NotificationNotFoundError,
    NotificationService,
)
from worker import NotificationWorker


def create_app(
    service: NotificationService | None = None,
    provider: LocalNotificationProvider | None = None,
) -> Flask:
    app = Flask(__name__)
    notification_service = service or NotificationService()
    local_provider = provider or LocalNotificationProvider()
    worker = NotificationWorker(notification_service, local_provider)
    app.extensions["notification_service"] = notification_service
    app.extensions["notification_provider"] = local_provider
    app.extensions["notification_worker"] = worker

    @app.after_request
    def add_response_headers(response):
        response.headers.setdefault("X-Request-ID", uuid4().hex)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("Cache-Control", "no-store")
        return response

    @app.post("/notifications")
    def create_notification():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify(error="request_body_must_be_json_object"), 400
        try:
            notification = notification_service.enqueue(
                recipient=payload.get("recipient"),
                channel=payload.get("channel"),
                message=payload.get("message"),
                idempotency_key=request.headers.get("Idempotency-Key") or payload.get("idempotency_key"),
            )
        except IdempotencyConflictError as exc:
            return jsonify(error="idempotency_conflict", message=str(exc)), 409
        except ValueError as exc:
            return jsonify(error="invalid_notification", message=str(exc)), 400
        return jsonify(notification.to_dict()), 202

    @app.get("/notifications/<notification_id>")
    def get_notification(notification_id: str):
        try:
            notification = notification_service.get(notification_id)
        except NotificationNotFoundError:
            return jsonify(error="notification_not_found"), 404
        return jsonify(notification.to_dict()), 200

    @app.post("/notifications/process-next")
    def process_next():
        processed = worker.process_one()
        return jsonify(processed=processed), 200

    return app


if __name__ == "__main__":
    create_app().run(debug=False)
