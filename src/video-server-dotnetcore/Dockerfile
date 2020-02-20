FROM mcr.microsoft.com/dotnet/core/aspnet:3.1.2-bionic AS base
WORKDIR /app

LABEL Name=grpc-video-server-dotnetcore Version=0.0.1
EXPOSE 80
EXPOSE 443
EXPOSE 5051

FROM mcr.microsoft.com/dotnet/core/sdk:3.1.102-bionic AS build
WORKDIR /src
COPY . .
RUN dotnet remove "video-server-dotnetcore/VideoServer.csproj" package OpenCvSharp4.runtime.win
RUN dotnet add "video-server-dotnetcore/VideoServer.csproj" package OpenCvSharp4.runtime.ubuntu.18.04-x64
RUN dotnet restore "video-server-dotnetcore/VideoServer.csproj"

WORKDIR "/src/video-server-dotnetcore"
RUN dotnet build "VideoServer.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "VideoServer.csproj" -c Release -o /app/publish

FROM base AS final
RUN apt-get update
RUN apt-get install -y libgtk2.0-dev
RUN apt-get -y update
RUN apt-get -y install wget unzip build-essential checkinstall cmake pkg-config yasm git gfortran libjpeg8-dev libpng-dev software-properties-common
RUN add-apt-repository "deb http://security.ubuntu.com/ubuntu xenial-security main"
RUN apt-get -y update && apt -y install libjasper1 libtiff-dev libavcodec-dev libavformat-dev libswscale-dev libdc1394-22-dev libxine2-dev libv4l-dev
RUN apt-get -y install libgtk2.0-dev libtbb-dev libatlas-base-dev libvorbis-dev libxvidcore-dev libopencore-amrnb-dev libopencore-amrwb-dev libavresample-dev x264 v4l-utils libwebp-dev tesseract-ocr libtesseract-dev libleptonica-dev

WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "VideoServer.dll"]