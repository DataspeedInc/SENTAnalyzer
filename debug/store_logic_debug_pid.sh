while ! ps ax | grep Logic | grep type=renderer > /dev/null
do
    sleep 0.5
done

ps ax | grep Logic | grep type=renderer | awk '{print $1}' > /tmp/logic_debug_pid