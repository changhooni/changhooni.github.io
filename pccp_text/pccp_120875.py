def solution(dots):
    answer = 0
    p1, p2, p3, p4 = dots[0], dots[1], dots[2], dots[3]
    
    s1 = get_slope(p1, p2)
    s2 = get_slope(p3, p4)
    if s1 == s2:
        answer = 1
        
    s3 = get_slope(p1, p3)
    s4 = get_slope(p2, p4)
    if s3 == s4:
        answer = 1
    
    s5 = get_slope(p1, p4)
    s6 = get_slope(p2, p3)
    if s5 == s6:
        answer = 1

    print(f"{s1}=={s2} // {s3}=={s4} // {s5}=={s6}")    
    return answer    

def get_slope(k1, k2)->int:
    print(f"({k2[1]} - {k1[1]}) * ({k2[0]} - {k1[0]}) = {(k2[1] - k1[1]) * (k2[0] - k1[0])}")
    return (k2[1] - k1[1]) * (k2[0] - k1[0])

data = [[3, 5], [4, 4], [8, 9], [6, 11]]
dot = solution(data)
print(dot)