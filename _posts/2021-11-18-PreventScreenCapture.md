---
title: "iOS 캡처 방지 TIP!"
strapline: "Swift"
description: "iOS 캡처방지"
header:
 overlay_image: /assets/images/triangular.jpeg
categories:
  - "Swift"
tag:
  - "swift"
  - "iOS"
  - "Prevent Screen Capture"
  - "캡처방지"
toc: true
last_modified_at: 2021-11-18
comments: true
mathjax: true
---

iOS에서 실질적으로 캡처를 방지할 수는 없습니다. (iOS의 OS에서 캡처를 담당하고 있으므로, 각 앱의 개발자가 할 수 있는 부분이 없음.)

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


<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1809380969362850"
     crossorigin="anonymous"></script>

<!-- 블로그 -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-1809380969362850"
     data-ad-slot="3200810651"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>

<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>