using System;
using System.Threading.Tasks;
using Grpc.Core;
using Microsoft.Extensions.Logging;
using OpenCvSharp;

namespace VideoServer.Services
{
    public class FramesReceiver : VideoFrame.VideoFrameBase
    {
        private readonly ILogger<FramesReceiver> logger;

        public FramesReceiver(ILogger<FramesReceiver> logger)
        {
            this.logger = logger;
        }

        public override async Task Send(IAsyncStreamReader<FrameRequest> requestStream,
            IServerStreamWriter<FrameReply> responseStream, ServerCallContext context)
        {
            VideoWriter writer = null;
            try
            {
                var requestsStream = requestStream.ReadAllAsync(context.CancellationToken);

                await foreach (var request in requestsStream)
                {
                    if (writer == null)
                        writer = new VideoWriter(".//widelo.avi", FourCCValues.DIVX, request.Fps,
                            new Size(request.Width, request.Height), request.IsColor);

                    var readMode = request.IsColor ? ImreadModes.Color : ImreadModes.Grayscale;
                    var frame = Cv2.ImDecode(request.Img.ToByteArray(), readMode);
                    writer.Write(frame);

                    await responseStream.WriteAsync(new FrameReply {Reply = 1});
                }
            }
            catch (Exception ex)
            {
                writer?.Release();
                Console.WriteLine(ex);
                Console.WriteLine("Exception occured when receiving frames");
            }
        }
    }
}