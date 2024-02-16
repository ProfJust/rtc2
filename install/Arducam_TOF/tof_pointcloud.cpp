#include <chrono>
#include <memory>
#include <string>
#include <sensor_msgs/msg/point_cloud.hpp>
#include <sensor_msgs/msg/point_cloud2.hpp>
#include <sensor_msgs/msg/point_field.hpp>
#include <rclcpp/rclcpp.hpp>

#include <std_msgs/msg/float32_multi_array.hpp>
#include <vector>

#include "ArducamTOFCamera.hpp"

using namespace std::chrono_literals;
using namespace Arducam;

ArducamTOFCamera tof;

class TOFPublisher : public rclcpp::Node
{
public:
//*** Konstruktor **//
    TOFPublisher() : Node("arducam"), pointsize_(43200)   
    {
        pc2_msg_ = std::make_shared<sensor_msgs::msg::PointCloud>();
        pc2_msg_->points.resize(pointsize_);
        pc2_msg_->channels.resize(1);
        pc2_msg_->channels[0].name = "intensities";
        pc2_msg_->channels[0].values.resize(pointsize_);
        // add PointCloud 2
        pc3_msg_ = std::make_shared<sensor_msgs::msg::PointCloud2>();
        
       /*  depth_msg_ = std::make_shared<std_msgs::msg::Float32MultiArray>();
        depth_msg_->layout.dim.resize(2);
        depth_msg_->layout.dim[0].label = "height";
        depth_msg_->layout.dim[0].size = 180;
        depth_msg_->layout.dim[0].stride = 43200;
        depth_msg_->layout.dim[1].label = "width";
        depth_msg_->layout.dim[1].size = 240;
        depth_msg_->layout.dim[1].stride = 240; */
        
        // publisher_ = this->create_publisher<sensor_msgs::msg::PointCloud>("point_cloud", 10);
        publisher_2 = this->create_publisher<sensor_msgs::msg::PointCloud2>("point_cloud2", 10);
        // publisher_depth_ = this->create_publisher<std_msgs::msg::Float32MultiArray>("depth_frame", 10);

        timer_ = this->create_wall_timer(
            100ms, std::bind(&TOFPublisher::update, this));  //OJU was 50ms
    }

private:
    void generateSensorPointCloud()
    {
        ArducamFrameBuffer *frame;
        do
        {
            frame = tof.requestFrame(200);  
        } while (frame == nullptr);
        depth_frame.clear();
        float *depth_ptr = (float *)frame->getData(FrameType::DEPTH_FRAME);
        float *amplitude_ptr = (float *)frame->getData(FrameType::AMPLITUDE_FRAME);
        unsigned long int pos = 0;
        for (int row_idx = 0; row_idx < 180; row_idx++)
            for (int col_idx = 0; col_idx < 240; col_idx++, pos++)
            {
                if (amplitude_ptr[pos] > 30)
                {
                    float zz = depth_ptr[pos]; 
                    pc2_msg_->points[pos].x = (((120 - col_idx)) / fx) * zz;
                    pc2_msg_->points[pos].y = ((90 - row_idx) / fy) * zz;
                    pc2_msg_->points[pos].z = zz;
                    pc2_msg_->channels[0].values[pos] = depth_ptr[pos];
                    depth_frame.push_back(depth_ptr[pos]);
                }
                else
                {
                    pc2_msg_->points[pos].x = 0;
                    pc2_msg_->points[pos].y = 0;
                    pc2_msg_->points[pos].z = 0;
                    pc2_msg_->channels[0].values[pos] = 0;
                    depth_frame.push_back(0);
                }
            }
        tof.releaseFrame(frame);
        pc2_msg_->header.frame_id = frame_id_;

       // depth_msg_->data = depth_frame;
    }
    void update()
    {
        generateSensorPointCloud();
        pc2_msg_->header.stamp = now();
        // publisher_->publish(*pc2_msg_);
        // Add Point Cloud2
        convertPointCloudToPointCloud2(*pc2_msg_, *pc3_msg_);
        publisher_2->publish(*pc3_msg_);
        // publisher_depth_->publish(*depth_msg_);
    }
    std::string frame_id_ = "sensor_frame";
    std::vector<float> depth_frame;
    sensor_msgs::msg::PointCloud::SharedPtr pc2_msg_;
    // Add PointCloud2
     sensor_msgs::msg::PointCloud2::SharedPtr pc3_msg_;
    //std_msgs::msg::Float32MultiArray::SharedPtr depth_msg_;

    size_t pointsize_;
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<sensor_msgs::msg::PointCloud>::SharedPtr publisher_;
    // Add PointCloud2
    rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr publisher_2;
    //rclcpp::Publisher<std_msgs::msg::Float32MultiArray>::SharedPtr publisher_depth_;

    float fx = 240 / (2 * tan(0.5 * M_PI * 64.3 / 180));
    float fy = 180 / (2 * tan(0.5 * M_PI * 50.4 / 180));

    //static inline 
    bool convertPointCloudToPointCloud2 (const sensor_msgs::msg::PointCloud &input, sensor_msgs::msg::PointCloud2 &output);
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    if (tof.open(Connection::CSI))
    {
        printf("initialize fail\n");
        exit(-1);
    }

    if (tof.start())
    {
        printf("start fail\n");
        exit(-1);
    }
    tof.setControl(CameraCtrl::RANGE,4);

    printf("pointcloud2 publisher start\n");

    setvbuf(stdout, NULL, _IONBF, BUFSIZ);
    rclcpp::spin(std::make_shared<TOFPublisher>());
    rclcpp::shutdown();
    tof.stop();
    tof.close();
    return 0;
}

//static inline 
bool TOFPublisher::convertPointCloudToPointCloud2 (const sensor_msgs::msg::PointCloud &input, sensor_msgs::msg::PointCloud2 &output)
{
   output.header = input.header;
   output.width  = input.points.size ();
   output.height = 1;
   output.fields.resize (3 + input.channels.size ());
   // Convert x/y/z to fields
   output.fields[0].name = "x"; output.fields[1].name = "y"; output.fields[2].name = "z";
   int offset = 0;
   // All offsets are *4, as all field data types are float32
   for (size_t d = 0; d < output.fields.size (); ++d, offset += 4){
     output.fields[d].offset = offset;
     output.fields[d].datatype = sensor_msgs::msg::PointField::FLOAT32;
     output.fields[d].count  = 1;
   }
   output.point_step = offset;
   output.row_step   = output.point_step * output.width;
   // Convert the remaining of the channels to fields
   for (size_t d = 0; d < input.channels.size (); ++d){
     output.fields[3 + d].name = input.channels[d].name;
   }
   output.data.resize (input.points.size () * output.point_step);
   output.is_bigendian = false;  // @todo ?
   output.is_dense     = false;

   // Copy the data points
    for (size_t cp = 0; cp < input.points.size (); ++cp){
      memcpy (&output.data[cp * output.point_step + output.fields[0].offset], &input.points[cp].x, sizeof (float));
      memcpy (&output.data[cp * output.point_step + output.fields[1].offset], &input.points[cp].y, sizeof (float));
      memcpy (&output.data[cp * output.point_step + output.fields[2].offset], &input.points[cp].z, sizeof (float));
      for (size_t d = 0; d < input.channels.size (); ++d){
        if (input.channels[d].values.size() == input.points.size()){
          memcpy (&output.data[cp * output.point_step + output.fields[3 + d].offset], &input.channels[d].values[cp], sizeof (float));
        }
      }
    }
  return (true);
}