#include <chrono>
#include <memory>
#include <string>
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
    std::string frame_id_ = "sensor_frame";
    std::vector<float> depth_frame;
    sensor_msgs::msg::PointCloud2::SharedPtr pc2_msg_;
    std_msgs::msg::Float32MultiArray::SharedPtr depth_msg_;
    size_t pointsize_ = 43200;
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr publisher_;
    rclcpp::Publisher<std_msgs::msg::Float32MultiArray>::SharedPtr publisher_depth_;

    float fx = 240 / (2 * tan(0.5 * M_PI * 64.3 / 180));
    float fy = 180 / (2 * tan(0.5 * M_PI * 50.4 / 180));


   //Konstruktor
    TOFPublisher() : Node("arducam")
    {
        pc2_msg_ = std::make_shared<sensor_msgs::msg::PointCloud2>();
        pc2_msg_->height =1;
        pc2_msg_->width = 43200; //.resize(pointsize_);

        depth_msg_ = std::make_shared<std_msgs::msg::Float32MultiArray>();
        depth_msg_->layout.dim.resize(2);
        depth_msg_->layout.dim[0].label = "height";
        depth_msg_->layout.dim[0].size = 180;
        depth_msg_->layout.dim[0].stride = 43200;
        depth_msg_->layout.dim[1].label = "width";
        depth_msg_->layout.dim[1].size = 240;
        depth_msg_->layout.dim[1].stride = 240;
        publisher_ = this->create_publisher<sensor_msgs::msg::PointCloud2>("point_cloud2", 10);
       //publisher_pointCloud2 = this->create_publisher<sensor_msgs::msg::PointCloud2>("point_cloud2", 10);
        publisher_depth_ = this->create_publisher<std_msgs::msg::Float32MultiArray>("depth_frame", 10);

        timer_ = this->create_wall_timer(
            50ms, std::bind(&TOFPublisher::update, this));
    }

private:
 void generateSensorPointCloud();
 void update();
};

void TOFPublisher::generateSensorPointCloud()
    {
        ArducamFrameBuffer *frame;
        do
        {
            frame = tof.requestFrame(200);
        } while (frame == nullptr);
        depth_frame.clear();
        // Get Data from Camera
        float *depth_ptr = (float *)frame->getData(FrameType::DEPTH_FRAME);
        float *amplitude_ptr = (float *)frame->getData(FrameType::AMPLITUDE_FRAME);

        // Build Message 

        pc2_msg_->is_bigendian = false;        
        pc2_msg_->is_dense = false;    

        // => SEGMENTATION FAULT
        pc2_msg_->fields[1].name     ="x"; // Name (String)
        pc2_msg_->fields[1].offset   = 0;  // Offset from start point of struct
        pc2_msg_->fields[1].datatype = sensor_msgs::msg::PointField::FLOAT32; 
        pc2_msg_->fields[1].count    = 1;   //43200;  //numb of Elements in Field


        pc2_msg_->point_step = 4;
        pc2_msg_->row_step = 4 * 43200;
         // <= SEGMENTATION FAULT

       for (unsigned long int i = 0; i < 180*240; i++){
           if (amplitude_ptr[i] > 30){
                float zz = depth_ptr[i];
                // pc2_msg_->fields.data[i]=zz;
                 depth_frame.push_back(depth_ptr[i]);
           }
           else{
             //pc2_msg_->fields.data[i]=0;
             depth_frame.push_back(0);
           }
        }

        tof.releaseFrame(frame);
        pc2_msg_->header.frame_id = frame_id_;

        depth_msg_->data = depth_frame;
    }


 void TOFPublisher::update()
    {
        generateSensorPointCloud();
        pc2_msg_->header.stamp = now();
        //pointCloud2_msg->header.stamp = now();
        publisher_->publish(*pc2_msg_);
        publisher_depth_->publish(*depth_msg_);
    }
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

    printf("pointcloud publisher start\n");

    setvbuf(stdout, NULL, _IONBF, BUFSIZ);
    rclcpp::spin(std::make_shared<TOFPublisher>());
    rclcpp::shutdown();
    tof.stop();
    tof.close();
    return 0;
}

