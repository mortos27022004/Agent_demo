#!/bin/bash

# Script để set OpenAI API key và chạy demo Agno
# Sử dụng: ./setup_and_run.sh

set -e  # Dừng nếu có lỗi



# Kiểm tra conda environment
if [ -z "$CONDA_DEFAULT_ENV" ] || [ "$CONDA_DEFAULT_ENV" != "agno-env" ]; then
    echo "⚠️  Conda environment 'agno-env' chưa được activate"
    echo "Đang activate..."
    
    # Source conda
    if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
        source "$HOME/miniconda3/etc/profile.d/conda.sh"
    else
        echo "❌ Không tìm thấy conda! Vui lòng activate manually:"
        echo "   conda activate agno-env"
        exit 1
    fi
    
    conda activate agno-env
    echo "✅ Đã activate environment: agno-env"
    echo
fi

# Chạy demo
echo "============================================================"
echo "🤖 Đang chạy demo..."
echo "============================================================"
echo



# Append thay vì ghi đè
python main.py 2>&1 | tee -a output.log

echo
echo "============================================================"
echo "✅ Script hoàn tất!"
echo "============================================================"
