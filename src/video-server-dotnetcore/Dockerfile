#See https://aka.ms/containerfastmode to understand how Visual Studio uses this Dockerfile to build your images for faster debugging.

FROM mcr.microsoft.com/dotnet/core/aspnet:3.1-buster-slim AS base
WORKDIR /app

LABEL Name=grpc-video-server-dotnetcore Version=0.0.1
EXPOSE 80
EXPOSE 443
EXPOSE 5051

FROM mcr.microsoft.com/dotnet/core/sdk:3.1-buster AS build
WORKDIR /src
COPY ["video-server-dotnetcore/VideoServer.csproj", "video-server-dotnetcore/"]
RUN dotnet restore "video-server-dotnetcore/VideoServer.csproj"
COPY . .
WORKDIR "/src/video-server-dotnetcore"
RUN dotnet build "VideoServer.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "VideoServer.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "VideoServer.dll"]