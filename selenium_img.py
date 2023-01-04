from selenium.webdriver.common.by import By
import shortuuid
from s3_connect import s3_connection, s3_img_upload, s3_get_img_url, default_img


def get_img(browser, url):
    # 쿠팡일 경우
    if (url.find("coupang.com") != -1):
        # 1. 이미지 스크래핑
        img_collector = browser.find_element(By.ID, "pdpImages")
        imgs = img_collector.find_elements(By.TAG_NAME, 'img')

    else:
        imgs = browser.find_elements(By.CSS_SELECTOR, 'img')

    for i in imgs:
        img = i.get_attribute("src")
        if 136 < img.__sizeof__()<= 400:
            break 

    #[todo] Img_url에 http,s 가 없는 경우 

    # 이미지 스크래핑 안되는 url은 캡처 후 s3에 올려서 이미지 url 생성
    if "data:image/svg+xml" in img:
        img = browser.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div[1]/div[1]/img')
        img_id = shortuuid.uuid()
        img.screenshot(f"./capture/kurly.{img_id}.png")
        filename = f"kurly.{img_id}.png"
        
        s3 = s3_connection()
        if s3:
            if s3_img_upload(s3, filename):
                img = s3_get_img_url(filename)
            else: # 이미지 불러오기 및 업로드로 url 요청 실패시 기본 이미지 url 반환
                img = default_img
        else:
            img = default_img

    # [todo] capture 폴더 안 이미지 시간되면 삭제할 수 있도록 스케줄링

    return img