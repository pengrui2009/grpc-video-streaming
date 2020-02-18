using System;
using System.Threading.Tasks;
using Grpc.Core;
using Microsoft.Extensions.Logging;

namespace VideoServerDotNetCore.Services
{
    public class FramesReceiver : VideoFrame.VideoFrameBase
    {
        private readonly ILogger<FramesReceiver> logger;

        public FramesReceiver(ILogger<FramesReceiver> logger)
        {
            this.logger = logger;
        }

        public override async Task Send(IAsyncStreamReader<FrameRequest> requestStream, IServerStreamWriter<FrameReply> responseStream, ServerCallContext context)
        {
            try
            {
                while (!context.CancellationToken.IsCancellationRequested)
                {
                    Console.WriteLine("Receive");
                    await responseStream.WriteAsync(new FrameReply { Reply = 1 });
                }
            }
            catch (System.Exception)
            {

                Console.WriteLine("Exception occured when receiving frames");
            }
        }
    }
}
