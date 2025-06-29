PYTHON=python3

LOG_FILE=proxy_log.txt
ALPHABET_FILE=alphabet.txt
MODEL_PDF=learned_model.pdf
SERVER_PORT=9100
PROXY_PORT=9101

.PHONY: all clean run_server run_proxy extract learn interactive

all: interactive

interactive: clean run_server run_proxy
	@echo ""
	@echo "Сервер и прокси запущены."
	@echo "Теперь введите команды как клиент (например, через nc 127.0.0.1 $(PROXY_PORT))"
	@echo "Когда закончите — нажмите ENTER здесь, чтобы продолжить обучение FSM."
	@read dummy; \
	echo "[make] Извлечение алфавита..."; \
	$(PYTHON) extract_alphabet.py; \
	echo "[make] Обучение FSM..."; \
	$(PYTHON) fsm_learner.py 127.0.0.1 $(SERVER_PORT)

run_server:
	@fuser -k $(SERVER_PORT)/tcp 2>/dev/null || true
	@echo "[make] Запуск booking_server.py..."
	@$(PYTHON) booking_server.py $(SERVER_PORT) &

run_proxy:
	@fuser -k $(PROXY_PORT)/tcp 2>/dev/null || true
	@echo "[make] Запуск proxy.py..."
	@$(PYTHON) proxy.py &

clean:
	@echo "[make] Очистка старых логов и моделей..."
	@rm -f $(LOG_FILE) $(ALPHABET_FILE) $(MODEL_PDF) learned_model.dot learned_model.json
