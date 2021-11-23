---
title: "iOS에서 인증번호 자동입력할 때 빈칸 클릭 때 크래쉬나는 문제 해결(NSTaggedPointerString Crash)"
strapline: "Swift"
description: "iOS에서 인증번호 자동입력할 때 빈칸 클릭 때 크래쉬나는 문제 해결(NSTaggedPointerString Crash)"
header:
 overlay_image: /assets/images/triangular.jpeg
categories:
  - "Swift"
tag:
  - "swift"
  - "iOS"
  - "swizzleReplacingCharacters"
  - "iOS 인증번호 자동입력"
toc: false
last_modified_at: 2021-11-22
comments: true
mathjax: true
---

iOS에서 인증번호 자동입력? 할 때, 아래 이미지의 빨간색 네모칸 터치 시에 앱이 크래쉬 나는 현상이 있습니다. 

<img src="https://user-images.githubusercontent.com/1383686/142784450-9ae31a46-f257-4af5-8551-f519f8626c64.PNG" style="zoom:50%;" />



이 부분은 최신 버전에서는 패치가 된 것으로 알고 있습니다. 

하지만, 특정 버전에서는 여전히 발생하는 문제이기 때문에 아래와 같은 소스로 해당 문제를 해결할 수 있습니다.

소스를 보시죠.

```swift
extension NSString {

    class func swizzleReplacingCharacters() {
        let originalMethod = class_getInstanceMethod(NSString.self, #selector(NSString.replacingCharacters(in:with:)))
        let swizzledMethod = class_getInstanceMethod(NSString.self, #selector(NSString.swizzledReplacingCharacters(in:with:)))

        guard let original = originalMethod, let swizzled = swizzledMethod else {
            return
        }

        method_exchangeImplementations(original, swizzled)
    }

    @objc
    func swizzledReplacingCharacters(in range: NSRange, with replacement: String) -> String {
        return self.swizzledReplacingCharacters(in: range, with: replacement)
    }
}
```



위와 같이 swizzle 관련 extension 을 구현 후,  AppDelegate 의 application 등의 적절한 위치에서 호출을 하여 줍니다.

```swift
func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        // Override point for customization after application launch.
  NSString.swizzleReplacingCharacters()
  return true
}
```




<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1809380969362850"
     crossorigin="anonymous"></script>