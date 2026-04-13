echo "Run Hyprland >>>>"

export WLR_NO_HARDWARE_CURSORS=1
export WLR_RENDERER_ALLOW_SOFTWARE=1
export XDG_SESSION_TYPE=wayland
export XDG_CURRENT_DESKTOP=Hyprland

if [ "$(whoami)" = "root" ]; then
    echo "→ Запуск от root. Переключаемся на пользователя weird..."
    
    # Самый простой и надёжный способ без sudo и su
    exec runuser -u weird -- Hyprland
else
    # Если уже запущен от обычного пользователя
    echo "→ Запуск от пользователя $(whoami)"
    exec Hyprland
fi
