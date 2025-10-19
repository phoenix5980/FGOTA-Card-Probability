import numpy as np
import time

def fgo_damage_simulation(card_values, threshold):
    assert len(card_values) == 4, "必须输入4个卡牌伤害值"
    card_values = np.array(card_values, dtype=np.float32)
    rand_values = np.linspace(0.900, 1.099, 200, dtype=np.float32)

    start = time.time()

    # 构造4维随机数组合
    R1, R2, R3, R4 = np.meshgrid(rand_values, rand_values, rand_values, rand_values, indexing='ij')

    # 总伤害
    total_damage = R1 * card_values[0] + R2 * card_values[1] + R3 * card_values[2] + R4 * card_values[3]

    # 正确的平均倍率（所有组合的平均倍率）
    total_random = (R1 + R2 + R3 + R4).mean() / 4

    # 成功率
    success_count = np.count_nonzero(total_damage >= threshold)
    total_count = total_damage.size
    success_rate = 100 * success_count / total_count

    print(f"▶ 总体随机数（平均倍率）：{total_random:.3f}")
    print(f"▶ 击破成功率：{success_rate:.3f}%")
    print(f"⏱️ 耗时：{time.time() - start:.2f} 秒")

    return total_random, success_rate

# 示例运行
fgo_damage_simulation([368658, 209168, 256827, 86019], threshold=999000)