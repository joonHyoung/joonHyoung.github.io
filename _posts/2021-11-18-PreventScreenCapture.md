---
header:
  image: /assets/images/posts/swift-capture.png
  teaser: /assets/images/posts/swift-capture.png
title: "iOS 캡처 방지 TIP!"
series: "iOS 트러블슈팅"
strapline: "Swift"
description: "iOS 앱에서 스크린샷·화면 녹화 시 특정 View만 가리는 방법 — isSecureTextEntry 텍스트 필드의 레이어를 이용한 makeSecure() 구현과 적용 예제, 주의사항"
categories:
  - "Swift"
tag:
  - "swift"
  - "iOS"
  - "Prevent Screen Capture"
  - "캡처방지"
toc: false
last_modified_at: 2026-10-30
comments: true
mathjax: true
---



iOS에서 실질적으로 캡처를 방지할 수는 없습니다. 

iOS의 OS에서 캡처를 담당하고 있으므로, 각 앱의 개발자가 할 수 있는 부분이 없습니다.

하지만, 캡처가 되는 순간에 캡처할 이미지를 변경하도록(투명화) 할 수 있습니다. 

다음 그림과 같이 말이죠. 

<img src="https://user-images.githubusercontent.com/1383686/142360934-a64c01a2-762d-4e35-bb2c-2e23273c3901.gif" style="zoom:20%;" />



보시는 것처럼, 초록색 View가 투명화? 처리되어 아래의 빨간 View만 스크린 캡처 되도록 할 수 있습니다.

그러면, 투명화? 처리를 하기 위해서 어떻게 해야 할지 아래의 소스를 보시죠.

```swift
extension UIView {
    func makeSecure() {
        DispatchQueue.main.async {
            let field = UITextField()
            field.isSecureTextEntry = true
            self.addSubview(field)
            field.centerYAnchor.constraint(equalTo: self.centerYAnchor).isActive = true
            field.centerXAnchor.constraint(equalTo: self.centerXAnchor).isActive = true
            self.layer.superlayer?.addSublayer(field.layer)
            field.layer.sublayers?.first?.addSublayer(self.layer)
        }
    }
}
```

위에 소스 처럼, makeSecure 를 구현 하고,  다음과 같이 적용 합니다. 

```swift
override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        
        secureView.makeSecure()
    }
```



이렇게 적용하고 나면, 사용자가 스크린 캡처시에 캡처되지 않을 부분을 설정 할 수 있습니다. 

[Github 소스](https://github.com/joonHyoung/preventScreenCapture)



## 동작 원리

iOS는 `isSecureTextEntry = true` 인 텍스트 필드(비밀번호 입력란)의 내용을 스크린샷과 화면 녹화에서 자동으로 가립니다.
`makeSecure()` 는 이 성질을 이용해, 보호하려는 View의 레이어를 보안 텍스트 필드의 내부 레이어 아래로 옮겨 붙입니다.
그러면 시스템이 그 View도 비밀번호 입력란의 일부로 취급해서 캡처 결과에서 빠지게 됩니다.

## 주의사항

- 보안 텍스트 필드의 **내부 레이어 구조**(`sublayers?.first`)에 기대는 방식이라 공식 API가 아닙니다. iOS 버전이 바뀌면 동작이 달라질 수 있으니, 새 iOS가 나올 때마다 실제 기기에서 다시 확인해야 합니다.
- 캡처 자체를 막는 것이 아니라 **특정 View만 비워서 찍히게** 하는 것입니다. 다른 기기의 카메라로 화면을 찍는 것까지 막을 수는 없습니다.

## 함께 쓰면 좋은 API

캡처를 감지해서 사용자에게 안내하거나 화면을 가리고 싶다면 아래 공식 API를 같이 사용할 수 있습니다.

- `UIApplication.userDidTakeScreenshotNotification`: 스크린샷을 찍은 **직후**에 알림을 받습니다. 찍히는 것을 막지는 못합니다.
- `UIScreen.main.isCaptured` / `UIScreen.capturedDidChangeNotification`: 화면 녹화나 미러링이 시작·종료될 때 알 수 있어서, 녹화 중에는 민감한 화면을 가리는 식으로 대응할 수 있습니다.
