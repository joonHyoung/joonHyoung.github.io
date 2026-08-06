# 로컬 개발용 Gemfile.
# CI 는 .github/Gemfile 을 쓴다(워크플로가 BUNDLE_GEMFILE 로 지정). 두 파일을 같은
# 구성으로 맞춰서 로컬 미리보기가 실제 배포와 동일한 결과를 내도록 한다.
#
# 예전에는 `gemspec` 한 줄이었다. 저장소에 gemspec 이 2개(minimal-mistakes-jekyll,
# plainwhite) 있어서 bundler 가 어느 쪽인지 판단하지 못해 에러를 냈고, 그래서
# 로컬 개발이 아예 불가능했다. 테마 gem 저장소 잔재를 걷어내면서 정상 Gemfile 로
# 교체했다.
source "https://rubygems.org"

gem "github-pages", group: :jekyll_plugins
gem "webrick"
