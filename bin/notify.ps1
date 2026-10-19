# Windows toast. Usage: powershell -NoProfile -ExecutionPolicy Bypass -File notify.ps1
# Reads the text from env vars CLAUDE_TOAST_TITLE and CLAUDE_TOAST_BODY (avoids quoting problems).
# Exit 0 when a toast was shown, 1 otherwise (notify.py then falls back to msg.exe).
try {
  [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
  $xml = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
  $t = $xml.GetElementsByTagName('text')
  $t.Item(0).AppendChild($xml.CreateTextNode($env:CLAUDE_TOAST_TITLE)) | Out-Null
  $t.Item(1).AppendChild($xml.CreateTextNode($env:CLAUDE_TOAST_BODY)) | Out-Null
  $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
  [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('Claude').Show($toast)
  exit 0
} catch { exit 1 }
