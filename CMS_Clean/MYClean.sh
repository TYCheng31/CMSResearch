#!/bin/bash

read -p "輸入要清理的 contest ID: " contest_id

read -p "確定要清除並重建 S01 ~ S75 的記錄？(y/n): " confirm

if [[ "$confirm" != "y" ]]; then
  echo "操作取消。"
  exit 1
fi

echo "Remove Participation..."
for i in $(seq -w 1 75); do
  cmsRemoveParticipation -c "$contest_id" S$i
done

echo "Add User..."
for i in $(seq -w 1 75); do
  cmsAddParticipation -c "$contest_id" S$i
done

echo "Finish"

