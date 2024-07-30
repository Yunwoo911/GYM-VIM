from django.shortcuts import render
from visitlogs.models import VisitLog
from django.utils import timezone
from gyms.models import GymMember
import datetime
from django.db.models import F
from account.models import CustomUser

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        login_user = request.user # customuser 테이블의 인스턴스
        # gym_id_list= GymMember.object.filter(user_id = login_user.user).values_list('gym_id', flat=True) # gym_id 목록
        # gym_id_list에는 리스트 형태로 gym_id 값들이 들어가있음
        # selected_gym_id =             # gym_id를 프론트엔드에서 선택하고 선택한 gym_id를 가져온다
        selected_gym_member = GymMember.objects.filter(user_id = login_user.user).last()
        selected_gym_id = selected_gym_member.gym_id

        # 출입기록 테이블에서 로그인한 유저의 헬스장 정보와 일치하는 레코드들을 가져온다.
        #                                                                       # enter_time이 현재시간보다 2시간전보다 미래                          # 퇴실시간이 아직 안된 회원
        read_gym_db = VisitLog.objects.filter(member__gym_id = selected_gym_id, enter_time__gte = timezone.now() - datetime.timedelta(hours=2), exit_time__gte = timezone.now())

        # 인원 카운트 
        # current_count는 read_gym_db의 길이
        # print(read_gym_db)
        current_count = read_gym_db.count()

        # 0으로 나누는 것을 방지하기 위한 체크
        exit_rate = login_user.manual_exit_rate

        context = {'current_count': current_count,'exit_rate': exit_rate}
        return render(request, 'home.html',context )

    
    

    # # exit_rate를 템플릿에 전달
    # return render(request, 'home.html', {'exit_rate': exit_rate})