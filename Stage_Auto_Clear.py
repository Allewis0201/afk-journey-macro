import cv2
import numpy as np
import pyautogui
import time
from screeninfo import get_monitors

# 모니터 해상도에 따른 이미지 경로 및 배율 설정
Monitor_check = 0
Monitors = get_monitors()
for monitor in Monitors:
    print(f"Monitor {monitor.name}: Resolution {monitor.width}x{monitor.height}")

print("_")
M_size = pyautogui.size()
M_resolution = str(M_size.width)


if M_resolution == "1920":
    R_1, R_2 = 1, 1
    AFK_Stage_Images_route = './Images/Stage_Auto_Clear_1920'
    print("해상도가 1920x1080입니다")
elif M_resolution == "2560":
    R_1, R_2 = 1.333333333333333, 1.333333333333333
    AFK_Stage_Images_route = './Images/Stage_Auto_Clear_2560'
    print("해상도가 2560x1440입니다")
else:
    print("죄송합니다. 지원하지 않는 해상도입니다")


# 이미지 매칭 함수
def find_image_on_screen(template_path, threshold=0.8):
    screenshot = pyautogui.screenshot()
    screen_img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)

    result = cv2.matchTemplate(screen_img, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        template_h, template_w = template.shape[:2]
        return max_loc[0] + template_w // 2, max_loc[1] + template_h // 2
    return None


# 매크로 실행 루프
Fail_count, Success_count = 0, 0

# 무한히 시도
for try_count in range(100000):
    stage_fail_count = 0
    stage_try_count = 0

    # 한 스테이지 반복
    for stage_try_count in range(100):
        clear_log_coords = find_image_on_screen(AFK_Stage_Images_route + '/Clear_Log.PNG', threshold=0.8)
        stage_fail_coords = find_image_on_screen(AFK_Stage_Images_route + '/Stage_Fail.PNG', threshold=0.8)
        stage_clear_coords = find_image_on_screen(AFK_Stage_Images_route + '/Stage_Clear.PNG', threshold=0.8)

        if clear_log_coords:
            print("클리어 로그 클릭")
            pyautogui.click(clear_log_coords)
            time.sleep(3)

            tmp_start = 0
            print("클리어 기록 선택")

            # 클리어 기록 선택
            while True:
                clear_log_arrow_right = find_image_on_screen(AFK_Stage_Images_route + '/Clear_Log_Arrow_Right.PNG',
                                                             threshold=0.8)
                
                # 다음 클리어 기록으로 이동
                while clear_log_arrow_right and tmp_start < stage_fail_count % 7:

                    pyautogui.click(clear_log_arrow_right)
                    time.sleep(2)
                    clear_log_arrow_right = find_image_on_screen(AFK_Stage_Images_route + '/Clear_Log_Arrow_Right.PNG',
                                                                 threshold=0.8)
                    tmp_start += 1

                print("진형 채택 시도")
                adoption_formation = find_image_on_screen(AFK_Stage_Images_route + '/Adoption_Formation.PNG', threshold=0.8)
                time.sleep(3)
                pyautogui.click(adoption_formation)
                time.sleep(3)


                # 미보유 영웅 및 메아리 존재 시 전투를 하지 않고 넘어감
                dont_have = find_image_on_screen(AFK_Stage_Images_route + '/Dont_Have.PNG', threshold=0.8)
                if dont_have:
                    print("미보유 영웅 및 메아리 존재")
                    dont_have_cancel = find_image_on_screen(AFK_Stage_Images_route + '/Dont_Have_Cancel.PNG', threshold=0.8)
                    stage_fail_count += 1

                    pyautogui.click(dont_have_cancel)
                    time.sleep(3)


                    # 제일 마지막 기록 실패 후 처음 기록으로 돌아감
                    clear_log_arrow_right = find_image_on_screen(AFK_Stage_Images_route + '/Clear_Log_Arrow_Right.PNG',
                                                                 threshold=0.8)
                    if clear_log_arrow_right is None:
                        clear_log_arrow_left = find_image_on_screen(AFK_Stage_Images_route + '/Clear_Log_Arrow_Left.PNG',
                                                                    threshold=0.8)
                        while clear_log_arrow_left and stage_fail_count % 7 == 0:
                            pyautogui.click(clear_log_arrow_left)
                            time.sleep(2)
                            clear_log_arrow_left = find_image_on_screen(AFK_Stage_Images_route + '/Clear_Log_Arrow_Left.PNG',
                                                                        threshold=0.8)
                        # 돌아가면서 시작 값 초기화
                        tmp_start = 0

                # 미보유 문제가 없다면 전투 처리로 넘어감
                else:
                    break

            # 전투 시작
            print("전투 시작")
            battle_start = find_image_on_screen(AFK_Stage_Images_route + '/Battle_Start.PNG', threshold=0.8)
            pyautogui.click(battle_start)
            time.sleep(3)

            # 진영 버프 미 배치 혹은 듀라 버프 영웅을 사용 하지 않아도 전투를 하도록 처리
            no_trait_bonus = find_image_on_screen(AFK_Stage_Images_route + '/No_Trait_Bonus.PNG', threshold=0.8)
            no_buff_hero = find_image_on_screen(AFK_Stage_Images_route + '/No_Buff_Hero.PNG', threshold=0.8)

            if no_trait_bonus or no_buff_hero:
                yes_button = find_image_on_screen(AFK_Stage_Images_route + '/Yes_Button.PNG', threshold=0.8)
                pyautogui.click(yes_button)
                time.sleep(3)


        # 전투 실패
        elif stage_fail_coords:
            print("전투 실패")
            stage_fail_count += 1
            battle_retry = find_image_on_screen(AFK_Stage_Images_route + '/Stage_Retry.PNG', threshold=0.8)
            time.sleep(3)
            pyautogui.click(battle_retry)

        # 스테이지 클리어 후 다음 스테이지로 이동
        elif stage_clear_coords:
            print("스테이지 클리어")
            next_stage = find_image_on_screen(AFK_Stage_Images_route + '/Next_Stage.PNG', threshold=0.8)
            next_dura = find_image_on_screen(AFK_Stage_Images_route + '/Next_Dura.PNG', threshold=0.8)
            next_tower = find_image_on_screen(AFK_Stage_Images_route + '/Next_Tower.PNG', threshold=0.8)
            time.sleep(3)


            if next_dura:
                pyautogui.click(next_dura)
                break
            elif next_tower:
                pyautogui.click(next_tower)
                break
            elif next_stage:
                pyautogui.click(next_stage)
                break

            break

        else:
            print("전투 중")
            time.sleep(2)