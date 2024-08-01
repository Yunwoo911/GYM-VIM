from django.shortcuts import render, redirect
from .models import VisitLog
from django.utils import timezone
from django.http import JsonResponse
from gyms.models import GymMember
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
import datetime
import pytz
import json
from django.db.models import F
from account.models import CustomUser
from django.urls import reverse
# 

# 현재 뷰의 문제점. 며칠 지난것도 퇴실이 가능할듯함 <-timezone.now().date()로 해결?

# 입실확인 뷰

# request.nfc_uid
def web_entrance(request):
    if request.method == 'POST':
        # taged_nfc_uid = request.POST.get('nfc_uid')
        enter_user = request.user
        which_member = GymMember.objects.filter(user=enter_user.user).last() # 로그인한 유저
        print(which_member)

        real_enter_time = timezone.now() 
        enter_log = VisitLog.objects.create(member_id = which_member.member_id, enter_time=real_enter_time,exit_time=real_enter_time + datetime.timedelta(hours=2))
        enter_log.save()
        return JsonResponse({'message': '입장이 완료되었습니다'})
    return JsonResponse({'message': '잘못된 요청'}, status=400)

def web_exit(request):
    if request.method == 'POST':
        try:
            # user는 요청을 보낸 유저
            login_user = request.user
            login_member = GymMember.objects.filter(user_id=login_user.user).last()
            exit_user = CustomUser.objects.get(user = login_user.user)
            # exit_log는 
            exit_log = VisitLog.objects.filter(member_id=login_member.member_id, exit_time__gte = timezone.now() - datetime.timedelta(hours=2)).last()
            if exit_log.exit_time < timezone.now():
                return JsonResponse({'message': "이미 퇴장 처리 되었습니다."})
            else:
                # 퇴장 시간은 버튼을 누른 시점
                exit_log.exit_time = timezone.now()
                exit_log.save()

                exit_user.gym_manual_exit_count = F('gym_manual_exit_count') + 1
                exit_user.manual_exit_rate = (exit_user.gym_manual_exit_count*0.1) / (exit_user.gym_entry_count*0.1) * 100
                exit_user.save()
                return JsonResponse({'message': '퇴장이 완료되었습니다'})
        except VisitLog.DoesNotExist:
            return JsonResponse({'message': '출입 기록이 없습니다.'})
    return JsonResponse({'message': '잘못된 요청'}, status=400)

        
# 입실인지 퇴실인지 확인하는 뷰

@csrf_exempt
def identify_nfc(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) # JSON 데이터를 파싱
        except json.JSONDecodeError:
            return JsonResponse({'error': '잘못된 11JSON 데이터입니다.'}, status=400)
        reader_gym_id = data.get('gym_id') # 입실 리더기에 고정된 gym_id를 가져온다.
        taged_nfc_uid = data.get('nfc_uid') # 입실 리더기로 읽은 nfc_uid를 가져온다.

        if not reader_gym_id: # reader_gym_id 없으면 에러
            return JsonResponse({'error': '헬스장 id가 없습니다.'}, status=400)
        if not taged_nfc_uid: # taged_nfc_uid 없으면 에러
            return JsonResponse({'error': 'nfc_uid가 없습니다.'}, status=400)
        
        try:
            which_user = CustomUser.objects.get(nfc_uid=taged_nfc_uid) # customuser 테이블에서 taged_nfc_uid로 어떤 유저인지 찾는다.
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': '해당 nfc_uid를 가진 사용자가 없습니다.'}, status=404)
        
        try:
            # which_member = GymMember.objects.get(gym_id=reader_gym_id, user=which_user.user)  # gymmember 테이블에서 gym_id와 user로 멤버인지 찾는다.
            # gymmember 상에서의 중복 오류 해결하기 전까지 임시 방편
            which_member = GymMember.objects.filter(gym_id=reader_gym_id, user=which_user.user).last()
        except GymMember.DoesNotExist:
            return JsonResponse({'error': '해당 헬스장에 등록된 사용자가 아닙니다.'}, status=404)
        # 조건
        # 누가 찍었는지를 알아야한다 => 들어온 nfc uid로 유저를 찾고, 그 유저의 user_id로 member_id를 찾는다
        # 찍은 유저의 입실 기록을 확인해야한다 => enter_time의 날짜가 오늘인지 or enter_time으로부터 2시간 이상 지났는지 확인
        # 상황 3개: 1. 아예 첫방문 or 오늘 첫방문 or 오늘 n번째 방문(마지막 입장시간으로부터 2시간 이상 지났는지 확인)
        # 생각해보니 아예 첫방문, 오늘 첫방문은 합쳐도 될듯?!?!?!?
        today = timezone.now().date()
        a = VisitLog.objects.filter(nfc_uid = taged_nfc_uid, member_id = which_member.member_id, enter_time__date = today).last()
        usa_tz = pytz.timezone('UTC')
        now_in_usa = timezone.now().astimezone(usa_tz)
        # 이 코드에 대해 말해보자면 마지막 입장시간이 지금으로부터 2시간보다 더 전이면 입장 url로 리다이렉트
        if a is None or a.enter_time < now_in_usa - datetime.timedelta(hours=2):
            return nfc_entrance(request, data)
        else:
            return nfc_exit(request, data)
    return JsonResponse({'error': '잘못된 요청'}, status=400)




@csrf_exempt
def nfc_entrance(request, data):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) # JSON 데이터를 파싱
        except json.JSONDecodeError:
            return JsonResponse({'error': '잘못된 JSON 데이터입니다.'}, status=400)
        reader_gym_id = data.get('gym_id') # 입실 리더기에 고정된 gym_id를 가져온다.
        taged_nfc_uid = data.get('nfc_uid') # 입실 리더기로 읽은 nfc_uid를 가져온다.
        
        if not reader_gym_id: # reader_gym_id 없으면 에러
            return JsonResponse({'error': '헬스장 id가 없습니다.'}, status=400)
        if not taged_nfc_uid: # taged_nfc_uid 없으면 에러
            return JsonResponse({'error': 'nfc_uid가 없습니다.'}, status=400)
        
        try:
            which_user = CustomUser.objects.get(nfc_uid=taged_nfc_uid) # customuser 테이블에서 taged_nfc_uid로 어떤 유저인지 찾는다.
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': '해당 nfc_uid를 가진 사용자가 없습니다.'}, status=404)
        
        try:
            # which_member = GymMember.objects.get(gym_id=reader_gym_id, user=which_user.user)  # gymmember 테이블에서 gym_id와 user로 멤버인지 찾는다.
            # gymmember 상에서의 중복 오류 해결하기 전까지 임시 방편
            which_member = GymMember.objects.filter(gym_id=reader_gym_id, user=which_user.user).last()
        except GymMember.DoesNotExist:
            return JsonResponse({'error': '해당 헬스장에 등록된 사용자가 아닙니다.'}, status=404)

        nfc_enter_time = timezone.now() # 현재 시간
        # 입실 기록 생성 + 2시간 후 퇴실 정보 저장
        enter_log = VisitLog.objects.create(nfc_uid=taged_nfc_uid, enter_time=nfc_enter_time, exit_time=nfc_enter_time + datetime.timedelta(hours=2), member_id= which_member.member_id)
        enter_log.save()
        # customuser의 gym_entry_count에 1을 추가하는 코드 필요
        # which_user.gym_entry_count += 1 
        which_user.gym_entry_count = F('gym_entry_count') + 1
        which_user.save()
        # save() 필요?
        return JsonResponse({'message': '입실이 완료되었습니다'})
    return JsonResponse({'error': '잘못된 요청'}, status=400)

@csrf_exempt
def nfc_exit(request, data):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) # JSON 데이터를 파싱
            # nfc 리더기로 부터 온 nfc_uid랑 gym_id
            taged_nfc_uid = data.get('nfc_uid')
            reader_gym_id = data.get('gym_id')
            
            # taged_user는 CustomUser 테이블에서 태그된 nfc_uid가 일치하는 유저 객체를 가져온다.
            which_user = CustomUser.objects.get(nfc_uid=taged_nfc_uid)
            # GymMember 테이블에서 태그된 유저, 헬스장 id를 가져옵니다(db 중복 문제때문에 코드를 주석처리 했습니다. 중복 문제 해결시 바로 아래 주석 풀고 97번째 코드 삭제 )
            # gym_member_id = GymMember.objects.get(user=taged_user.user, gym_id=reader_gym_id).member_id
            which_member = GymMember.objects.filter(gym_id=reader_gym_id, user=which_user.user).last() # 중복 문제 해결시 삭제
            # exit_log는 VisitLog 테이블에서 퇴실기록(자동퇴실: 입장시간으로부터 2시간 뒤), 이 현재 시간에서 2시간 이내에 퇴장 기록이 없으면.
            exit_log = VisitLog.objects.filter(member_id=which_member.member_id, exit_time__gte = timezone.now() - datetime.timedelta(hours=2)).last()

            visit_log = VisitLog.objects.filter(member_id = which_member.member_id)
            recent_log = visit_log.last() # 가장 최신 기록
            if recent_log.exit_time == timezone.now():
                return JsonResponse({'message': '2시간이 경과하여 자동 퇴실되었습니다.'})
            else:# 퇴장시간이 미래 -> 아직 퇴장하지 않았다
                recent_log.exit_time = timezone.now()
                recent_log.save() # 퇴장 시간에 현재 시간을 저장
                which_user.gym_manual_exit_count = F('gym_manual_exit_count') + 1
                which_user.manual_exit_rate = (which_user.gym_manual_exit_count*0.1) / (which_user.gym_entry_count*0.1) * 100
                which_user.save()
                return JsonResponse({'message': '퇴장이 완료되었습니다'})  

            # if exit_log.exit_time < timezone.now():
            #     return JsonResponse({'message': "이미 퇴장 처리 되었습니다."})
            # else:
            #     exit_log.exit_time = timezone.now() # 퇴장 시간은 버튼을 누른 시점
            #     exit_log.save() # 퇴장 기록 DB에 저장
            # which_user.gym_manual_exit_count = F('gym_manual_exit_count') + 1
            # which_user.save()

            # gym_entry_count 는 어떻게보면 총 입장 횟수
            # 그럼 퇴장시에도 manual_exit_count를 하나씩 +1 굿
            # exit_rate는 수동 퇴장률이니깐 입장횟수  
            return JsonResponse({'message': '퇴장이 완료되었습니다'})
        except VisitLog.DoesNotExist:
            return JsonResponse({'message': '입장 기록이 없습니다.'})   
    return JsonResponse({'message': '잘못된 요청'}, status=400)


#nfc 입퇴실 통합
@csrf_exempt
def nfc_enter_exit(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) # JSON 데이터를 파싱
        except json.JSONDecodeError:
            return JsonResponse({'error': '잘못된 JSON 데이터입니다.'}, status=400)
        reader_gym_id = data.get('gym_id') # 입실 리더기에 고정된 gym_id를 가져온다.
        taged_nfc_uid = data.get('nfc_uid') # 입실 리더기로 읽은 nfc_uid를 가져온다.
        
        if not reader_gym_id: # reader_gym_id 없으면 에러
            return JsonResponse({'error': '헬스장 id가 없습니다.'}, status=400)
        if not taged_nfc_uid: # taged_nfc_uid 없으면 에러
            return JsonResponse({'error': 'nfc_uid가 없습니다.'}, status=400)
        
        try:
            which_user = CustomUser.objects.get(nfc_uid=taged_nfc_uid) # customuser 테이블에서 taged_nfc_uid로 어떤 유저인지 찾는다.
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': '해당 nfc_uid를 가진 사용자가 없습니다.'}, status=404)
        
    
        try:
            # which_member = GymMember.objects.get(gym_id=reader_gym_id, user=which_user.user)  # gymmember 테이블에서 gym_id와 user로 멤버인지 찾는다.
            # gymmember 상에서의 중복 오류 해결하기 전까지 임시 방편
            which_member = GymMember.objects.filter(gym_id=reader_gym_id, user=which_user.user).last()
        except GymMember.DoesNotExist:
            return JsonResponse({'error': '해당 헬스장에 등록된 사용자가 아닙니다.'}, status=404)
                    
        visit_log = VisitLog.objects.filter(member_id = which_member.member_id)
        nfc_enter_time = timezone.now()
        if not visit_log: # 입퇴장로그가 없는 경우 -> 신규회원
            # 입실 기록 생성 + 2시간 후 퇴실 정보 저장
            enter_log = VisitLog.objects.create(nfc_uid=taged_nfc_uid, enter_time=nfc_enter_time, exit_time=nfc_enter_time + datetime.timedelta(hours=2), member_id= which_member.member_id)
            enter_log.save() #입장 처리
            which_user.gym_entry_count = F('gym_entry_count') + 1
            which_user.save()
            return JsonResponse({'message': '입실이 완료되었습니다'})
        else: #입퇴장 로그가 존재
            recent_log = visit_log.last() # 가장 최신 기록
            if recent_log.exit_time < timezone.now(): # 퇴장시간이 과거 -> 이미 퇴장 했고 nfc 태그를 입장 요청으로 분류
                enter_log = VisitLog.objects.create(nfc_uid=taged_nfc_uid, enter_time=nfc_enter_time, exit_time=nfc_enter_time + datetime.timedelta(hours=2), member_id= which_member.member_id)
                enter_log.save()
                which_user.gym_entry_count = F('gym_entry_count') + 1
                which_user.save()
                return JsonResponse({'message': '입실이 완료되었습니다'})
            elif recent_log.exit_time == timezone.now():
                return JsonResponse({'message': '2시간이 경과하여 자동 퇴실되었습니다.'})
            else:# 퇴장시간이 미래 -> 아직 퇴장하지 않았다
                recent_log.exit_time = timezone.now()
                recent_log.save() # 퇴장 시간에 현재 시간을 저장
                which_user.gym_manual_exit_count = F('gym_manual_exit_count') + 1
                which_user.manual_exit_rate = (which_user.gym_manual_exit_count*0.1) / (which_user.gym_entry_count*0.1) * 100
                which_user.save()
                return JsonResponse({'message': '퇴장이 완료되었습니다'})  
    return JsonResponse({'error': '잘못된 요청'}, status=400)


# visitlog 테이블을 조회해서 enter_time이 현재시간으로부터 2시간 이내이고, exit_time이 현재시간보다 미래인 경우
# 실시간 인원 확인 뷰
# def current_member(request):
#     login_user = request.user # customuser 테이블의 인스턴스
#     # gym_id_list= GymMember.object.filter(user_id = login_user.user).values_list('gym_id', flat=True) # gym_id 목록
#     # gym_id_list에는 리스트 형태로 gym_id 값들이 들어가있음
#     # selected_gym_id =             # gym_id를 프론트엔드에서 선택하고 선택한 gym_id를 가져온다
#     selected_gym_member = GymMember.objects.filter(user_id = login_user.user).last()
#     selected_gym_id = selected_gym_member.gym_id

#     # 출입기록 테이블에서 로그인한 유저의 헬스장 정보와 일치하는 레코드들을 가져온다.
#     #                                                                       # enter_time이 현재시간보다 2시간전보다 미래                          # 퇴실시간이 아직 안된 회원
#     read_gym_db = VisitLog.objects.filter(member__gym_id = selected_gym_id, enter_time__gte = timezone.now() - datetime.timedelta(hours=2), exit_time__gte = timezone.now())

#     # 인원 카운트 
#     # current_count는 read_gym_db의 길이
#     current_count = read_gym_db.count()
#     # print(current_count)
#     return render(request, 'home.html', {'current_count': current_count})

# 예약, 입퇴실
# nfc 여진님이 진행중이셔서 그동안 다른 기구예약이나, 웹퇴실버튼, 자동퇴실

# 입퇴실 받는 고유번호를
# nfc_uid로 or user_id로

# 회원정보에 user_id
# nfc_uid 퇴실 인식필드로 사용하는쪽으로 가기로 했었는데

# 2단계 정도 건너뛰어서 말씀드림

# 커스텀유저 키로 받는가?