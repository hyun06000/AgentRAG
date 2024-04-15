uvicorn main:master --reload --port 8000 &
uvicorn search_master:search_master --reload --port 8001 &
uvicorn article_researcher:article_researcher --reload --port 8002 &
uvicorn article_parser:article_parser --reload --port 8003 &
sleep 3

wait

sleep 3

#clear

PIDS=($(pgrep -f uvicorn))

echo "killing uvicorn process: ${PIDS[@]}"
for PID in "${PIDS[@]}"
do
    kill -9 "$PID"
done