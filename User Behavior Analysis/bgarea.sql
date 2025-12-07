/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80034
 Source Host           : localhost:3306
 Source Schema         : bgarea

 Target Server Type    : MySQL
 Target Server Version : 80034
 File Encoding         : 65001

 Date: 08/12/2025 01:07:59
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for course_knowledge
-- ----------------------------
DROP TABLE IF EXISTS `course_knowledge`;
CREATE TABLE `course_knowledge`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `course_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `knowledge_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '知识点ID',
  `knowledge_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '知识点名称',
  `prerequisite_knowledge` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '先修知识点（逗号分隔）',
  `difficulty` tinyint(0) NULL DEFAULT NULL COMMENT '知识点难度',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `course_id`(`course_id`) USING BTREE,
  CONSTRAINT `course_knowledge_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '课程知识点表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of course_knowledge
-- ----------------------------
INSERT INTO `course_knowledge` VALUES (1, 'C001', 'K001', 'Python变量', '', 1);
INSERT INTO `course_knowledge` VALUES (2, 'C001', 'K002', 'Python循环', 'K001', 2);
INSERT INTO `course_knowledge` VALUES (3, 'C002', 'K003', 'Pandas数据读取', 'K002', 3);
INSERT INTO `course_knowledge` VALUES (4, 'C002', 'K004', '数据清洗', 'K003', 3);
INSERT INTO `course_knowledge` VALUES (5, 'C004', 'K006', 'Requests库使用', 'K001', 2);
INSERT INTO `course_knowledge` VALUES (6, 'C005', 'K007', 'Excel自动化', 'K002', 4);
INSERT INTO `course_knowledge` VALUES (7, 'C006', 'K008', 'Java基础语法', '', 1);
INSERT INTO `course_knowledge` VALUES (8, 'C007', 'K009', 'Servlet开发', 'K008', 3);
INSERT INTO `course_knowledge` VALUES (9, 'C009', 'K010', 'SQL基本查询', '', 2);
INSERT INTO `course_knowledge` VALUES (10, 'C010', 'K011', '索引优化', 'K010', 4);
INSERT INTO `course_knowledge` VALUES (11, 'C011', 'K011', '唐诗基础', '', 1);
INSERT INTO `course_knowledge` VALUES (12, 'C012', 'K012', '鲁迅作品分析', '', 2);
INSERT INTO `course_knowledge` VALUES (13, 'C013', 'K013', '莎士比亚戏剧', 'K011', 3);
INSERT INTO `course_knowledge` VALUES (14, 'C013', 'K014', '托尔斯泰小说解读', 'K012', 3);
INSERT INTO `course_knowledge` VALUES (15, 'C014', 'K015', '宋词格律', 'K011', 4);
INSERT INTO `course_knowledge` VALUES (16, 'C015', 'K016', '文学评论写作', 'K013,K014', 5);
INSERT INTO `course_knowledge` VALUES (17, 'C016', 'K017', 'Pandas可视化', 'K003', 3);
INSERT INTO `course_knowledge` VALUES (18, 'C017', 'K018', 'Scikit-learn入门', 'K017', 4);
INSERT INTO `course_knowledge` VALUES (19, 'C018', 'K019', 'TensorFlow实战', 'K018', 5);
INSERT INTO `course_knowledge` VALUES (20, 'C019', 'K020', 'FastAPI开发', 'K002', 3);
INSERT INTO `course_knowledge` VALUES (21, 'C020', 'K021', 'Ansible自动化', 'K001', 4);
INSERT INTO `course_knowledge` VALUES (22, 'C021', 'K022', 'SpringBoot配置', 'K008', 3);
INSERT INTO `course_knowledge` VALUES (23, 'C022', 'K023', 'SpringCloud组件', 'K022', 4);
INSERT INTO `course_knowledge` VALUES (24, 'C023', 'K024', '分布式锁实现', 'K023', 5);
INSERT INTO `course_knowledge` VALUES (25, 'C024', 'K025', '链表与树', 'K008', 2);
INSERT INTO `course_knowledge` VALUES (26, 'C025', 'K026', '单例模式', 'K025', 4);
INSERT INTO `course_knowledge` VALUES (27, 'C026', 'K027', 'ACID原则', 'K010', 3);
INSERT INTO `course_knowledge` VALUES (28, 'C027', 'K028', 'Sharding-JDBC', 'K027', 4);
INSERT INTO `course_knowledge` VALUES (29, 'C028', 'K029', '索引类型', 'K010', 3);
INSERT INTO `course_knowledge` VALUES (30, 'C029', 'K030', 'mysqldump备份', 'K010', 2);
INSERT INTO `course_knowledge` VALUES (31, 'C030', 'K031', 'EXPLAIN分析', 'K029', 5);
INSERT INTO `course_knowledge` VALUES (32, 'C031', 'K032', '五四文学', 'K012', 3);
INSERT INTO `course_knowledge` VALUES (33, 'C032', 'K033', '跨文化比较', 'K013', 4);
INSERT INTO `course_knowledge` VALUES (34, 'C033', 'K034', '民间故事类型', 'K011', 2);
INSERT INTO `course_knowledge` VALUES (35, 'C034', 'K035', '叙事学理论', 'K032', 3);
INSERT INTO `course_knowledge` VALUES (36, 'C035', 'K036', '网络小说结构', 'K034', 4);

-- ----------------------------
-- Table structure for courses
-- ----------------------------
DROP TABLE IF EXISTS `courses`;
CREATE TABLE `courses`  (
  `course_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '课程唯一ID',
  `course_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '课程名称',
  `difficulty` tinyint(0) NULL DEFAULT NULL COMMENT '难度等级：1-5',
  `domain` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '学科领域',
  `created_at` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`course_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '课程表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of courses
-- ----------------------------
INSERT INTO `courses` VALUES ('C001', 'Python零基础入门', 1, 'Python', '2025-12-07 20:54:11');
INSERT INTO `courses` VALUES ('C002', 'Python数据分析实战', 3, 'Python', '2025-12-07 20:54:11');
INSERT INTO `courses` VALUES ('C003', 'Python高级编程', 5, 'Python', '2025-12-07 20:54:11');
INSERT INTO `courses` VALUES ('C004', 'Python爬虫入门', 2, 'Python', '2025-12-07 20:54:11');
INSERT INTO `courses` VALUES ('C005', 'Python自动化办公', 4, 'Python', '2025-12-07 20:54:11');
INSERT INTO `courses` VALUES ('C006', 'Java零基础入门', 1, 'Java', '2025-12-07 20:54:11');
INSERT INTO `courses` VALUES ('C007', 'JavaWeb开发', 3, 'Java', '2025-12-07 20:54:11');
INSERT INTO `courses` VALUES ('C008', 'Java并发编程', 5, 'Java', '2025-12-07 20:54:11');
INSERT INTO `courses` VALUES ('C009', 'MySQL基础入门', 2, 'MySQL', '2025-12-07 20:54:11');
INSERT INTO `courses` VALUES ('C010', 'MySQL高级优化', 4, 'MySQL', '2025-12-07 20:54:11');
INSERT INTO `courses` VALUES ('C011', '中国古代文学入门', 1, '文学', '2025-12-07 21:14:20');
INSERT INTO `courses` VALUES ('C012', '中国现代文学赏析', 2, '文学', '2025-12-07 21:14:20');
INSERT INTO `courses` VALUES ('C013', '外国经典文学解读', 3, '文学', '2025-12-07 21:14:20');
INSERT INTO `courses` VALUES ('C014', '古诗词鉴赏进阶', 4, '文学', '2025-12-07 21:14:20');
INSERT INTO `courses` VALUES ('C015', '文学创作与评论', 5, '文学', '2025-12-07 21:14:20');
INSERT INTO `courses` VALUES ('C016', 'Python数据分析可视化', 3, 'Python', '2025-12-07 21:24:27');
INSERT INTO `courses` VALUES ('C017', 'Python机器学习入门', 4, 'Python', '2025-12-07 21:24:27');
INSERT INTO `courses` VALUES ('C018', 'Python深度学习实战', 5, 'Python', '2025-12-07 21:24:27');
INSERT INTO `courses` VALUES ('C019', 'Python接口开发', 3, 'Python', '2025-12-07 21:24:27');
INSERT INTO `courses` VALUES ('C020', 'Python运维自动化', 4, 'Python', '2025-12-07 21:24:27');
INSERT INTO `courses` VALUES ('C021', 'JavaSpringBoot入门', 3, 'Java', '2025-12-07 21:24:27');
INSERT INTO `courses` VALUES ('C022', 'Java微服务开发', 4, 'Java', '2025-12-07 21:24:27');
INSERT INTO `courses` VALUES ('C023', 'Java分布式架构', 5, 'Java', '2025-12-07 21:24:27');
INSERT INTO `courses` VALUES ('C024', 'Java数据结构', 2, 'Java', '2025-12-07 21:24:27');
INSERT INTO `courses` VALUES ('C025', 'Java设计模式', 4, 'Java', '2025-12-07 21:24:27');
INSERT INTO `courses` VALUES ('C026', 'MySQL事务与锁', 3, 'MySQL', '2025-12-07 21:24:27');
INSERT INTO `courses` VALUES ('C027', 'MySQL分库分表', 4, 'MySQL', '2025-12-07 21:24:27');
INSERT INTO `courses` VALUES ('C028', 'MySQL索引优化实战', 3, 'MySQL', '2025-12-07 21:24:27');
INSERT INTO `courses` VALUES ('C029', 'MySQL数据备份恢复', 2, 'MySQL', '2025-12-07 21:24:27');
INSERT INTO `courses` VALUES ('C030', 'MySQL性能调优', 5, 'MySQL', '2025-12-07 21:24:27');
INSERT INTO `courses` VALUES ('C031', '现当代文学思潮', 3, '文学', '2025-12-07 21:24:27');
INSERT INTO `courses` VALUES ('C032', '比较文学导论', 4, '文学', '2025-12-07 21:24:27');
INSERT INTO `courses` VALUES ('C033', '民间文学研究', 2, '文学', '2025-12-07 21:24:27');
INSERT INTO `courses` VALUES ('C034', '文学理论基础', 3, '文学', '2025-12-07 21:24:27');
INSERT INTO `courses` VALUES ('C035', '网络文学创作', 4, '文学', '2025-12-07 21:24:27');

-- ----------------------------
-- Table structure for user_behaviors
-- ----------------------------
DROP TABLE IF EXISTS `user_behaviors`;
CREATE TABLE `user_behaviors`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '行为ID',
  `user_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户ID',
  `course_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '课程ID',
  `chapter_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '章节ID',
  `behavior_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '行为类型：video_play/video_pause/video_forward/video_slow/video_finish',
  `behavior_detail` json NOT NULL COMMENT '行为详情（结构化JSON）',
  `behavior_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP COMMENT '行为时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `course_id`(`course_id`) USING BTREE,
  INDEX `idx_user_course_type`(`user_id`, `course_id`, `behavior_type`) USING BTREE,
  CONSTRAINT `user_behaviors_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `user_behaviors_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户行为表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_behaviors
-- ----------------------------
INSERT INTO `user_behaviors` VALUES (1, 'U001', 'C002', '', 'click', '{\"click_count\": 3}', '2025-12-07 20:54:23');
INSERT INTO `user_behaviors` VALUES (2, 'U001', 'C002', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 20:54:23');
INSERT INTO `user_behaviors` VALUES (3, 'U001', 'C002', '', 'video_play', '{\"play_duration\": 600}', '2025-12-07 20:54:23');
INSERT INTO `user_behaviors` VALUES (4, 'U001', 'C002', '', 'video_pause', '{\"pause_second\": 120}', '2025-12-07 20:54:23');
INSERT INTO `user_behaviors` VALUES (5, 'U001', 'C002', '', 'video_finish', '{\"complete_rate\": 0.67}', '2025-12-07 20:54:23');
INSERT INTO `user_behaviors` VALUES (6, 'U001', 'C002', '', 'answer_submit', '{\"is_correct\": 0, \"spend_time\": 70, \"knowledge_id\": \"K003\"}', '2025-12-07 20:54:23');
INSERT INTO `user_behaviors` VALUES (7, 'U001', 'C002', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 65, \"knowledge_id\": \"K002\"}', '2025-12-07 20:54:23');
INSERT INTO `user_behaviors` VALUES (8, 'U004', 'C004', '', 'click', '{\"click_count\": 2}', '2025-12-07 20:54:28');
INSERT INTO `user_behaviors` VALUES (9, 'U004', 'C004', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 20:54:28');
INSERT INTO `user_behaviors` VALUES (10, 'U004', 'C004', '', 'video_finish', '{\"complete_rate\": 0.9}', '2025-12-07 20:54:28');
INSERT INTO `user_behaviors` VALUES (11, 'U004', 'C004', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 30, \"knowledge_id\": \"K006\"}', '2025-12-07 20:54:28');
INSERT INTO `user_behaviors` VALUES (12, 'U002', 'C007', '', 'click', '{\"click_count\": 4}', '2025-12-07 20:54:32');
INSERT INTO `user_behaviors` VALUES (13, 'U002', 'C007', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 20:54:32');
INSERT INTO `user_behaviors` VALUES (14, 'U002', 'C007', '', 'video_finish', '{\"complete_rate\": 1.0}', '2025-12-07 20:54:32');
INSERT INTO `user_behaviors` VALUES (15, 'U002', 'C007', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 25, \"knowledge_id\": \"K008\"}', '2025-12-07 20:54:32');
INSERT INTO `user_behaviors` VALUES (16, 'U006', 'C013', '', 'click', '{\"click_count\": 5}', '2025-12-07 21:14:26');
INSERT INTO `user_behaviors` VALUES (17, 'U006', 'C013', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:14:26');
INSERT INTO `user_behaviors` VALUES (18, 'U006', 'C013', '', 'video_play', '{\"play_duration\": 1200}', '2025-12-07 21:14:26');
INSERT INTO `user_behaviors` VALUES (19, 'U006', 'C013', '', 'video_finish', '{\"complete_rate\": 0.85}', '2025-12-07 21:14:26');
INSERT INTO `user_behaviors` VALUES (20, 'U006', 'C013', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 45, \"knowledge_id\": \"K013\"}', '2025-12-07 21:14:26');
INSERT INTO `user_behaviors` VALUES (21, 'U006', 'C013', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 50, \"knowledge_id\": \"K014\"}', '2025-12-07 21:14:26');
INSERT INTO `user_behaviors` VALUES (22, 'U007', 'C012', '', 'click', '{\"click_count\": 3}', '2025-12-07 21:14:29');
INSERT INTO `user_behaviors` VALUES (23, 'U007', 'C012', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:14:29');
INSERT INTO `user_behaviors` VALUES (24, 'U007', 'C012', '', 'video_finish', '{\"complete_rate\": 0.9}', '2025-12-07 21:14:29');
INSERT INTO `user_behaviors` VALUES (25, 'U007', 'C012', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 30, \"knowledge_id\": \"K012\"}', '2025-12-07 21:14:29');
INSERT INTO `user_behaviors` VALUES (26, 'U001', 'C004', '', 'click', '{\"click_count\": 4}', '2025-12-07 21:24:34');
INSERT INTO `user_behaviors` VALUES (27, 'U001', 'C004', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:24:34');
INSERT INTO `user_behaviors` VALUES (28, 'U001', 'C004', '', 'video_finish', '{\"complete_rate\": 0.9}', '2025-12-07 21:24:34');
INSERT INTO `user_behaviors` VALUES (29, 'U001', 'C005', '', 'click', '{\"click_count\": 3}', '2025-12-07 21:24:34');
INSERT INTO `user_behaviors` VALUES (30, 'U001', 'C005', '', 'video_play', '{\"play_duration\": 800}', '2025-12-07 21:24:34');
INSERT INTO `user_behaviors` VALUES (31, 'U001', 'C016', '', 'click', '{\"click_count\": 5}', '2025-12-07 21:24:34');
INSERT INTO `user_behaviors` VALUES (32, 'U001', 'C016', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 40}', '2025-12-07 21:24:34');
INSERT INTO `user_behaviors` VALUES (33, 'U001', 'C017', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:24:34');
INSERT INTO `user_behaviors` VALUES (34, 'U001', 'C017', '', 'video_pause', '{\"pause_second\": 150}', '2025-12-07 21:24:34');
INSERT INTO `user_behaviors` VALUES (35, 'U001', 'C019', '', 'click', '{\"click_count\": 2}', '2025-12-07 21:24:34');
INSERT INTO `user_behaviors` VALUES (36, 'U008', 'C001', '', 'click', '{\"click_count\": 6}', '2025-12-07 21:24:38');
INSERT INTO `user_behaviors` VALUES (37, 'U008', 'C001', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:24:38');
INSERT INTO `user_behaviors` VALUES (38, 'U008', 'C004', '', 'video_finish', '{\"complete_rate\": 0.8}', '2025-12-07 21:24:38');
INSERT INTO `user_behaviors` VALUES (39, 'U008', 'C016', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 35}', '2025-12-07 21:24:38');
INSERT INTO `user_behaviors` VALUES (40, 'U008', 'C018', '', 'click', '{\"click_count\": 4}', '2025-12-07 21:24:38');
INSERT INTO `user_behaviors` VALUES (41, 'U008', 'C020', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:24:38');
INSERT INTO `user_behaviors` VALUES (42, 'U008', 'C020', '', 'video_play', '{\"play_duration\": 900}', '2025-12-07 21:24:38');
INSERT INTO `user_behaviors` VALUES (43, 'U008', 'C017', '', 'answer_submit', '{\"is_correct\": 0, \"spend_time\": 50}', '2025-12-07 21:24:38');
INSERT INTO `user_behaviors` VALUES (44, 'U009', 'C002', '', 'click', '{\"click_count\": 3}', '2025-12-07 21:24:45');
INSERT INTO `user_behaviors` VALUES (45, 'U009', 'C002', '', 'video_finish', '{\"complete_rate\": 0.75}', '2025-12-07 21:24:45');
INSERT INTO `user_behaviors` VALUES (46, 'U009', 'C016', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:24:45');
INSERT INTO `user_behaviors` VALUES (47, 'U009', 'C019', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 45}', '2025-12-07 21:24:45');
INSERT INTO `user_behaviors` VALUES (48, 'U009', 'C020', '', 'click', '{\"click_count\": 5}', '2025-12-07 21:24:45');
INSERT INTO `user_behaviors` VALUES (49, 'U010', 'C003', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:24:45');
INSERT INTO `user_behaviors` VALUES (50, 'U010', 'C003', '', 'video_play', '{\"play_duration\": 1000}', '2025-12-07 21:24:45');
INSERT INTO `user_behaviors` VALUES (51, 'U010', 'C017', '', 'click', '{\"click_count\": 4}', '2025-12-07 21:24:45');
INSERT INTO `user_behaviors` VALUES (52, 'U010', 'C018', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 60}', '2025-12-07 21:24:45');
INSERT INTO `user_behaviors` VALUES (53, 'U010', 'C016', '', 'video_finish', '{\"complete_rate\": 0.9}', '2025-12-07 21:24:45');
INSERT INTO `user_behaviors` VALUES (54, 'U011', 'C004', '', 'click', '{\"click_count\": 7}', '2025-12-07 21:24:45');
INSERT INTO `user_behaviors` VALUES (55, 'U011', 'C005', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:24:45');
INSERT INTO `user_behaviors` VALUES (56, 'U011', 'C019', '', 'video_play', '{\"play_duration\": 850}', '2025-12-07 21:24:45');
INSERT INTO `user_behaviors` VALUES (57, 'U011', 'C017', '', 'answer_submit', '{\"is_correct\": 0, \"spend_time\": 40}', '2025-12-07 21:24:45');
INSERT INTO `user_behaviors` VALUES (58, 'U011', 'C020', '', 'video_finish', '{\"complete_rate\": 0.85}', '2025-12-07 21:24:45');
INSERT INTO `user_behaviors` VALUES (59, 'U012', 'C001', '', 'video_finish', '{\"complete_rate\": 0.95}', '2025-12-07 21:24:45');
INSERT INTO `user_behaviors` VALUES (60, 'U012', 'C002', '', 'click', '{\"click_count\": 4}', '2025-12-07 21:24:45');
INSERT INTO `user_behaviors` VALUES (61, 'U012', 'C016', '', 'video_play', '{\"play_duration\": 700}', '2025-12-07 21:24:45');
INSERT INTO `user_behaviors` VALUES (62, 'U012', 'C018', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:24:45');
INSERT INTO `user_behaviors` VALUES (63, 'U012', 'C019', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 30}', '2025-12-07 21:24:45');
INSERT INTO `user_behaviors` VALUES (64, 'U002', 'C006', '', 'click', '{\"click_count\": 5}', '2025-12-07 21:24:49');
INSERT INTO `user_behaviors` VALUES (65, 'U002', 'C006', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:24:49');
INSERT INTO `user_behaviors` VALUES (66, 'U002', 'C021', '', 'video_finish', '{\"complete_rate\": 0.8}', '2025-12-07 21:24:49');
INSERT INTO `user_behaviors` VALUES (67, 'U002', 'C022', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 45}', '2025-12-07 21:24:49');
INSERT INTO `user_behaviors` VALUES (68, 'U002', 'C024', '', 'click', '{\"click_count\": 3}', '2025-12-07 21:24:49');
INSERT INTO `user_behaviors` VALUES (69, 'U002', 'C025', '', 'video_play', '{\"play_duration\": 900}', '2025-12-07 21:24:49');
INSERT INTO `user_behaviors` VALUES (70, 'U013', 'C007', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:24:56');
INSERT INTO `user_behaviors` VALUES (71, 'U013', 'C007', '', 'video_finish', '{\"complete_rate\": 0.75}', '2025-12-07 21:24:56');
INSERT INTO `user_behaviors` VALUES (72, 'U013', 'C021', '', 'click', '{\"click_count\": 4}', '2025-12-07 21:24:56');
INSERT INTO `user_behaviors` VALUES (73, 'U013', 'C023', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 50}', '2025-12-07 21:24:56');
INSERT INTO `user_behaviors` VALUES (74, 'U013', 'C025', '', 'video_play', '{\"play_duration\": 800}', '2025-12-07 21:24:56');
INSERT INTO `user_behaviors` VALUES (75, 'U014', 'C006', '', 'video_finish', '{\"complete_rate\": 0.9}', '2025-12-07 21:24:56');
INSERT INTO `user_behaviors` VALUES (76, 'U014', 'C008', '', 'click', '{\"click_count\": 6}', '2025-12-07 21:24:56');
INSERT INTO `user_behaviors` VALUES (77, 'U014', 'C022', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:24:56');
INSERT INTO `user_behaviors` VALUES (78, 'U014', 'C024', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 35}', '2025-12-07 21:24:56');
INSERT INTO `user_behaviors` VALUES (79, 'U014', 'C021', '', 'video_play', '{\"play_duration\": 750}', '2025-12-07 21:24:56');
INSERT INTO `user_behaviors` VALUES (80, 'U015', 'C007', '', 'click', '{\"click_count\": 5}', '2025-12-07 21:24:56');
INSERT INTO `user_behaviors` VALUES (81, 'U015', 'C021', '', 'video_finish', '{\"complete_rate\": 0.85}', '2025-12-07 21:24:56');
INSERT INTO `user_behaviors` VALUES (82, 'U015', 'C023', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:24:56');
INSERT INTO `user_behaviors` VALUES (83, 'U015', 'C025', '', 'answer_submit', '{\"is_correct\": 0, \"spend_time\": 40}', '2025-12-07 21:24:56');
INSERT INTO `user_behaviors` VALUES (84, 'U015', 'C022', '', 'click', '{\"click_count\": 4}', '2025-12-07 21:24:56');
INSERT INTO `user_behaviors` VALUES (85, 'U016', 'C008', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:24:56');
INSERT INTO `user_behaviors` VALUES (86, 'U016', 'C022', '', 'video_play', '{\"play_duration\": 950}', '2025-12-07 21:24:56');
INSERT INTO `user_behaviors` VALUES (87, 'U016', 'C024', '', 'click', '{\"click_count\": 3}', '2025-12-07 21:24:56');
INSERT INTO `user_behaviors` VALUES (88, 'U016', 'C023', '', 'video_finish', '{\"complete_rate\": 0.7}', '2025-12-07 21:24:56');
INSERT INTO `user_behaviors` VALUES (89, 'U016', 'C021', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 55}', '2025-12-07 21:24:56');
INSERT INTO `user_behaviors` VALUES (90, 'U003', 'C009', '', 'click', '{\"click_count\": 6}', '2025-12-07 21:25:02');
INSERT INTO `user_behaviors` VALUES (91, 'U003', 'C009', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:25:02');
INSERT INTO `user_behaviors` VALUES (92, 'U003', 'C010', '', 'video_finish', '{\"complete_rate\": 0.8}', '2025-12-07 21:25:02');
INSERT INTO `user_behaviors` VALUES (93, 'U003', 'C026', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 45}', '2025-12-07 21:25:02');
INSERT INTO `user_behaviors` VALUES (94, 'U003', 'C028', '', 'video_play', '{\"play_duration\": 800}', '2025-12-07 21:25:02');
INSERT INTO `user_behaviors` VALUES (95, 'U017', 'C009', '', 'video_finish', '{\"complete_rate\": 0.9}', '2025-12-07 21:25:02');
INSERT INTO `user_behaviors` VALUES (96, 'U017', 'C026', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:25:02');
INSERT INTO `user_behaviors` VALUES (97, 'U017', 'C027', '', 'click', '{\"click_count\": 4}', '2025-12-07 21:25:02');
INSERT INTO `user_behaviors` VALUES (98, 'U017', 'C029', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 35}', '2025-12-07 21:25:02');
INSERT INTO `user_behaviors` VALUES (99, 'U017', 'C030', '', 'video_play', '{\"play_duration\": 900}', '2025-12-07 21:25:02');
INSERT INTO `user_behaviors` VALUES (100, 'U018', 'C010', '', 'click', '{\"click_count\": 5}', '2025-12-07 21:25:02');
INSERT INTO `user_behaviors` VALUES (101, 'U018', 'C028', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:25:02');
INSERT INTO `user_behaviors` VALUES (102, 'U018', 'C029', '', 'video_finish', '{\"complete_rate\": 0.85}', '2025-12-07 21:25:02');
INSERT INTO `user_behaviors` VALUES (103, 'U018', 'C030', '', 'answer_submit', '{\"is_correct\": 0, \"spend_time\": 40}', '2025-12-07 21:25:02');
INSERT INTO `user_behaviors` VALUES (104, 'U018', 'C026', '', 'click', '{\"click_count\": 3}', '2025-12-07 21:25:02');
INSERT INTO `user_behaviors` VALUES (105, 'U006', 'C011', '', 'click', '{\"click_count\": 5}', '2025-12-07 21:25:08');
INSERT INTO `user_behaviors` VALUES (106, 'U006', 'C011', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:25:08');
INSERT INTO `user_behaviors` VALUES (107, 'U006', 'C012', '', 'video_finish', '{\"complete_rate\": 0.8}', '2025-12-07 21:25:08');
INSERT INTO `user_behaviors` VALUES (108, 'U006', 'C031', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 45}', '2025-12-07 21:25:08');
INSERT INTO `user_behaviors` VALUES (109, 'U006', 'C033', '', 'video_play', '{\"play_duration\": 800}', '2025-12-07 21:25:08');
INSERT INTO `user_behaviors` VALUES (110, 'U007', 'C011', '', 'video_finish', '{\"complete_rate\": 0.9}', '2025-12-07 21:25:08');
INSERT INTO `user_behaviors` VALUES (111, 'U007', 'C013', '', 'click', '{\"click_count\": 6}', '2025-12-07 21:25:08');
INSERT INTO `user_behaviors` VALUES (112, 'U007', 'C031', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:25:08');
INSERT INTO `user_behaviors` VALUES (113, 'U007', 'C034', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 35}', '2025-12-07 21:25:08');
INSERT INTO `user_behaviors` VALUES (114, 'U007', 'C032', '', 'video_play', '{\"play_duration\": 750}', '2025-12-07 21:25:08');
INSERT INTO `user_behaviors` VALUES (115, 'U019', 'C012', '', 'click', '{\"click_count\": 5}', '2025-12-07 21:25:08');
INSERT INTO `user_behaviors` VALUES (116, 'U019', 'C014', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:25:08');
INSERT INTO `user_behaviors` VALUES (117, 'U019', 'C032', '', 'video_finish', '{\"complete_rate\": 0.85}', '2025-12-07 21:25:08');
INSERT INTO `user_behaviors` VALUES (118, 'U019', 'C035', '', 'answer_submit', '{\"is_correct\": 0, \"spend_time\": 40}', '2025-12-07 21:25:08');
INSERT INTO `user_behaviors` VALUES (119, 'U019', 'C031', '', 'click', '{\"click_count\": 4}', '2025-12-07 21:25:08');
INSERT INTO `user_behaviors` VALUES (120, 'U020', 'C015', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:25:08');
INSERT INTO `user_behaviors` VALUES (121, 'U020', 'C033', '', 'video_play', '{\"play_duration\": 950}', '2025-12-07 21:25:08');
INSERT INTO `user_behaviors` VALUES (122, 'U020', 'C034', '', 'click', '{\"click_count\": 3}', '2025-12-07 21:25:08');
INSERT INTO `user_behaviors` VALUES (123, 'U020', 'C032', '', 'video_finish', '{\"complete_rate\": 0.7}', '2025-12-07 21:25:08');
INSERT INTO `user_behaviors` VALUES (124, 'U020', 'C031', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 55}', '2025-12-07 21:25:08');
INSERT INTO `user_behaviors` VALUES (125, 'U004', 'C001', '', 'click', '{\"click_count\": 4}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (126, 'U004', 'C001', '', 'video_finish', '{\"complete_rate\": 0.85}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (127, 'U004', 'C002', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (128, 'U004', 'C003', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 40}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (129, 'U004', 'C016', '', 'video_play', '{\"play_duration\": 700}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (130, 'U010', 'C004', '', 'click', '{\"click_count\": 5}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (131, 'U010', 'C005', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (132, 'U010', 'C019', '', 'video_finish', '{\"complete_rate\": 0.9}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (133, 'U010', 'C020', '', 'answer_submit', '{\"is_correct\": 0, \"spend_time\": 50}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (134, 'U011', 'C001', '', 'video_play', '{\"play_duration\": 600}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (135, 'U011', 'C002', '', 'click', '{\"click_count\": 3}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (136, 'U011', 'C017', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (137, 'U011', 'C018', '', 'video_finish', '{\"complete_rate\": 0.8}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (138, 'U012', 'C003', '', 'click', '{\"click_count\": 6}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (139, 'U012', 'C005', '', 'video_play', '{\"play_duration\": 800}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (140, 'U012', 'C016', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (141, 'U012', 'C017', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 35}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (142, 'U008', 'C002', '', 'video_pause', '{\"pause_second\": 120}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (143, 'U008', 'C003', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 45}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (144, 'U008', 'C016', '', 'click', '{\"click_count\": 7}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (145, 'U008', 'C018', '', 'video_finish', '{\"complete_rate\": 0.75}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (146, 'U008', 'C019', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (147, 'U009', 'C001', '', 'video_play', '{\"play_duration\": 900}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (148, 'U009', 'C005', '', 'click', '{\"click_count\": 4}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (149, 'U009', 'C017', '', 'video_pause', '{\"pause_second\": 150}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (150, 'U009', 'C020', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 55}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (151, 'U010', 'C001', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (152, 'U010', 'C018', '', 'click', '{\"click_count\": 5}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (153, 'U011', 'C003', '', 'video_finish', '{\"complete_rate\": 0.85}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (154, 'U011', 'C019', '', 'answer_submit', '{\"is_correct\": 0, \"spend_time\": 40}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (155, 'U012', 'C002', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (156, 'U012', 'C018', '', 'video_play', '{\"play_duration\": 750}', '2025-12-07 21:34:00');
INSERT INTO `user_behaviors` VALUES (157, 'U004', 'C001', '', 'click', '{\"click_count\": 4}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (158, 'U004', 'C001', '', 'video_finish', '{\"complete_rate\": 0.85}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (159, 'U004', 'C002', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (160, 'U004', 'C003', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 40}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (161, 'U004', 'C016', '', 'video_play', '{\"play_duration\": 700}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (162, 'U010', 'C004', '', 'click', '{\"click_count\": 5}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (163, 'U010', 'C005', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (164, 'U010', 'C019', '', 'video_finish', '{\"complete_rate\": 0.9}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (165, 'U010', 'C020', '', 'answer_submit', '{\"is_correct\": 0, \"spend_time\": 50}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (166, 'U011', 'C001', '', 'video_play', '{\"play_duration\": 600}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (167, 'U011', 'C002', '', 'click', '{\"click_count\": 3}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (168, 'U011', 'C017', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (169, 'U011', 'C018', '', 'video_finish', '{\"complete_rate\": 0.8}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (170, 'U012', 'C003', '', 'click', '{\"click_count\": 6}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (171, 'U012', 'C005', '', 'video_play', '{\"play_duration\": 800}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (172, 'U012', 'C016', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (173, 'U012', 'C017', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 35}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (174, 'U008', 'C002', '', 'video_pause', '{\"pause_second\": 120}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (175, 'U008', 'C003', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 45}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (176, 'U008', 'C016', '', 'click', '{\"click_count\": 7}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (177, 'U008', 'C018', '', 'video_finish', '{\"complete_rate\": 0.75}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (178, 'U008', 'C019', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (179, 'U009', 'C001', '', 'video_play', '{\"play_duration\": 900}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (180, 'U009', 'C005', '', 'click', '{\"click_count\": 4}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (181, 'U009', 'C017', '', 'video_pause', '{\"pause_second\": 150}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (182, 'U009', 'C020', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 55}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (183, 'U010', 'C001', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (184, 'U010', 'C018', '', 'click', '{\"click_count\": 5}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (185, 'U011', 'C003', '', 'video_finish', '{\"complete_rate\": 0.85}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (186, 'U011', 'C019', '', 'answer_submit', '{\"is_correct\": 0, \"spend_time\": 40}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (187, 'U012', 'C002', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (188, 'U012', 'C018', '', 'video_play', '{\"play_duration\": 750}', '2025-12-07 21:34:11');
INSERT INTO `user_behaviors` VALUES (189, 'U005', 'C006', '', 'click', '{\"click_count\": 5}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (190, 'U005', 'C007', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (191, 'U005', 'C021', '', 'video_finish', '{\"complete_rate\": 0.8}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (192, 'U005', 'C022', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 45}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (193, 'U013', 'C006', '', 'video_play', '{\"play_duration\": 700}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (194, 'U013', 'C008', '', 'click', '{\"click_count\": 3}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (195, 'U013', 'C023', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (196, 'U013', 'C024', '', 'video_finish', '{\"complete_rate\": 0.9}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (197, 'U014', 'C007', '', 'click', '{\"click_count\": 6}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (198, 'U014', 'C021', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (199, 'U014', 'C022', '', 'video_play', '{\"play_duration\": 800}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (200, 'U014', 'C025', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 35}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (201, 'U015', 'C006', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (202, 'U015', 'C008', '', 'video_finish', '{\"complete_rate\": 0.85}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (203, 'U015', 'C023', '', 'click', '{\"click_count\": 4}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (204, 'U015', 'C024', '', 'answer_submit', '{\"is_correct\": 0, \"spend_time\": 40}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (205, 'U016', 'C007', '', 'video_play', '{\"play_duration\": 900}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (206, 'U016', 'C021', '', 'click', '{\"click_count\": 5}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (207, 'U016', 'C022', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (208, 'U016', 'C023', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 50}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (209, 'U002', 'C023', '', 'click', '{\"click_count\": 7}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (210, 'U002', 'C024', '', 'video_play', '{\"play_duration\": 600}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (211, 'U002', 'C025', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (212, 'U013', 'C025', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 45}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (213, 'U014', 'C023', '', 'video_pause', '{\"pause_second\": 120}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (214, 'U015', 'C021', '', 'click', '{\"click_count\": 6}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (215, 'U015', 'C025', '', 'video_finish', '{\"complete_rate\": 0.75}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (216, 'U016', 'C024', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (217, 'U005', 'C023', '', 'video_play', '{\"play_duration\": 850}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (218, 'U005', 'C024', '', 'answer_submit', '{\"is_correct\": 0, \"spend_time\": 55}', '2025-12-07 21:34:34');
INSERT INTO `user_behaviors` VALUES (219, 'U005', 'C006', '', 'click', '{\"click_count\": 5}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (220, 'U005', 'C007', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (221, 'U005', 'C021', '', 'video_finish', '{\"complete_rate\": 0.8}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (222, 'U005', 'C022', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 45}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (223, 'U013', 'C006', '', 'video_play', '{\"play_duration\": 700}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (224, 'U013', 'C008', '', 'click', '{\"click_count\": 3}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (225, 'U013', 'C023', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (226, 'U013', 'C024', '', 'video_finish', '{\"complete_rate\": 0.9}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (227, 'U014', 'C007', '', 'click', '{\"click_count\": 6}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (228, 'U014', 'C021', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (229, 'U014', 'C022', '', 'video_play', '{\"play_duration\": 800}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (230, 'U014', 'C025', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 35}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (231, 'U015', 'C006', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (232, 'U015', 'C008', '', 'video_finish', '{\"complete_rate\": 0.85}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (233, 'U015', 'C023', '', 'click', '{\"click_count\": 4}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (234, 'U015', 'C024', '', 'answer_submit', '{\"is_correct\": 0, \"spend_time\": 40}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (235, 'U016', 'C007', '', 'video_play', '{\"play_duration\": 900}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (236, 'U016', 'C021', '', 'click', '{\"click_count\": 5}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (237, 'U016', 'C022', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (238, 'U016', 'C023', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 50}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (239, 'U002', 'C023', '', 'click', '{\"click_count\": 7}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (240, 'U002', 'C024', '', 'video_play', '{\"play_duration\": 600}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (241, 'U002', 'C025', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (242, 'U013', 'C025', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 45}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (243, 'U014', 'C023', '', 'video_pause', '{\"pause_second\": 120}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (244, 'U015', 'C021', '', 'click', '{\"click_count\": 6}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (245, 'U015', 'C025', '', 'video_finish', '{\"complete_rate\": 0.75}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (246, 'U016', 'C024', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (247, 'U005', 'C023', '', 'video_play', '{\"play_duration\": 850}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (248, 'U005', 'C024', '', 'answer_submit', '{\"is_correct\": 0, \"spend_time\": 55}', '2025-12-07 21:34:39');
INSERT INTO `user_behaviors` VALUES (249, 'U003', 'C026', '', 'click', '{\"click_count\": 5}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (250, 'U003', 'C027', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (251, 'U003', 'C029', '', 'video_finish', '{\"complete_rate\": 0.8}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (252, 'U003', 'C030', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 45}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (253, 'U017', 'C009', '', 'video_play', '{\"play_duration\": 700}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (254, 'U017', 'C010', '', 'click', '{\"click_count\": 3}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (255, 'U017', 'C028', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (256, 'U017', 'C029', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 35}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (257, 'U018', 'C009', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (258, 'U018', 'C026', '', 'video_finish', '{\"complete_rate\": 0.85}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (259, 'U018', 'C027', '', 'click', '{\"click_count\": 4}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (260, 'U018', 'C028', '', 'answer_submit', '{\"is_correct\": 0, \"spend_time\": 40}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (261, 'U006', 'C014', '', 'click', '{\"click_count\": 6}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (262, 'U006', 'C015', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (263, 'U006', 'C032', '', 'video_finish', '{\"complete_rate\": 0.9}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (264, 'U006', 'C034', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 50}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (265, 'U007', 'C014', '', 'video_play', '{\"play_duration\": 800}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (266, 'U007', 'C015', '', 'click', '{\"click_count\": 5}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (267, 'U007', 'C033', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (268, 'U007', 'C035', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 35}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (269, 'U019', 'C011', '', 'click', '{\"click_count\": 7}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (270, 'U019', 'C013', '', 'video_finish', '{\"complete_rate\": 0.85}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (271, 'U019', 'C031', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (272, 'U019', 'C032', '', 'answer_submit', '{\"is_correct\": 0, \"spend_time\": 45}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (273, 'U020', 'C012', '', 'video_play', '{\"play_duration\": 900}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (274, 'U020', 'C014', '', 'click', '{\"click_count\": 4}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (275, 'U020', 'C034', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (276, 'U020', 'C035', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 55}', '2025-12-07 21:34:58');
INSERT INTO `user_behaviors` VALUES (277, 'U001', 'C018', '', 'click', '{\"click_count\": 5}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (278, 'U001', 'C020', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (279, 'U004', 'C017', '', 'video_finish', '{\"complete_rate\": 0.8}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (280, 'U004', 'C019', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 40}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (281, 'U008', 'C004', '', 'video_play', '{\"play_duration\": 700}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (282, 'U008', 'C005', '', 'click', '{\"click_count\": 3}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (283, 'U009', 'C016', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (284, 'U009', 'C018', '', 'answer_submit', '{\"is_correct\": 0, \"spend_time\": 50}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (285, 'U002', 'C022', '', 'video_play', '{\"play_duration\": 800}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (286, 'U002', 'C023', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (287, 'U005', 'C022', '', 'click', '{\"click_count\": 6}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (288, 'U005', 'C024', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 35}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (289, 'U013', 'C022', '', 'video_finish', '{\"complete_rate\": 0.85}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (290, 'U014', 'C024', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (291, 'U003', 'C028', '', 'video_play', '{\"play_duration\": 600}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (292, 'U003', 'C029', '', 'click', '{\"click_count\": 4}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (293, 'U017', 'C030', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (294, 'U018', 'C030', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 45}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (295, 'U006', 'C031', '', 'video_play', '{\"play_duration\": 900}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (296, 'U006', 'C033', '', 'click', '{\"click_count\": 5}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (297, 'U007', 'C031', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (298, 'U019', 'C033', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 50}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (299, 'U001', 'C003', '', 'video_pause', '{\"pause_second\": 120}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (300, 'U001', 'C017', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 40}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (301, 'U002', 'C006', '', 'video_play', '{\"play_duration\": 750}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (302, 'U002', 'C025', '', 'click', '{\"click_count\": 7}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (303, 'U003', 'C010', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (304, 'U003', 'C027', '', 'answer_submit', '{\"is_correct\": 0, \"spend_time\": 55}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (305, 'U004', 'C003', '', 'video_finish', '{\"complete_rate\": 0.8}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (306, 'U004', 'C018', '', 'click', '{\"click_count\": 6}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (307, 'U005', 'C008', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (308, 'U005', 'C023', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 45}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (309, 'U006', 'C035', '', 'video_play', '{\"play_duration\": 800}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (310, 'U006', 'C015', '', 'click', '{\"click_count\": 4}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (311, 'U007', 'C034', '', 'video_finish', '{\"complete_rate\": 0.85}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (312, 'U007', 'C014', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 35}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (313, 'U008', 'C017', '', 'video_pause', '{\"pause_second\": 150}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (314, 'U009', 'C019', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (315, 'U010', 'C020', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 50}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (316, 'U011', 'C004', '', 'video_play', '{\"play_duration\": 700}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (317, 'U012', 'C005', '', 'click', '{\"click_count\": 5}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (318, 'U013', 'C007', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (319, 'U014', 'C006', '', 'answer_submit', '{\"is_correct\": 0, \"spend_time\": 40}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (320, 'U015', 'C022', '', 'video_play', '{\"play_duration\": 850}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (321, 'U016', 'C023', '', 'click', '{\"click_count\": 6}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (322, 'U017', 'C026', '', 'collect', '{\"is_cancel\": 0}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (323, 'U018', 'C027', '', 'answer_submit', '{\"is_correct\": 1, \"spend_time\": 45}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (324, 'U019', 'C032', '', 'video_play', '{\"play_duration\": 900}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (325, 'U020', 'C033', '', 'click', '{\"click_count\": 4}', '2025-12-07 21:35:23');
INSERT INTO `user_behaviors` VALUES (335, 'U001', 'C002', 'CH001', 'video_play', '{\"speed\": 1.0, \"start_second\": 0, \"play_duration\": 120}', '2025-12-08 09:00:00');
INSERT INTO `user_behaviors` VALUES (336, 'U002', 'C002', 'CH001', 'video_play', '{\"speed\": 1.0, \"start_second\": 0, \"play_duration\": 90}', '2025-12-08 09:05:00');
INSERT INTO `user_behaviors` VALUES (337, 'U001', 'C002', 'CH001', 'video_pause', '{\"duration\": 5, \"pause_second\": 30}', '2025-12-08 09:00:30');
INSERT INTO `user_behaviors` VALUES (338, 'U002', 'C002', 'CH001', 'video_pause', '{\"duration\": 10, \"pause_second\": 45}', '2025-12-08 09:06:15');
INSERT INTO `user_behaviors` VALUES (339, 'U001', 'C002', 'CH001', 'video_forward', '{\"speed\": 2.0, \"end_second\": 90, \"start_second\": 60}', '2025-12-08 09:02:00');
INSERT INTO `user_behaviors` VALUES (340, 'U003', 'C002', 'CH001', 'video_forward', '{\"speed\": 1.5, \"end_second\": 120, \"start_second\": 80}', '2025-12-08 09:10:00');
INSERT INTO `user_behaviors` VALUES (341, 'U002', 'C002', 'CH001', 'video_slow', '{\"speed\": 0.5, \"end_second\": 40, \"start_second\": 20}', '2025-12-08 09:07:00');
INSERT INTO `user_behaviors` VALUES (342, 'U003', 'C002', 'CH001', 'video_slow', '{\"speed\": 0.8, \"end_second\": 70, \"start_second\": 50}', '2025-12-08 09:11:00');
INSERT INTO `user_behaviors` VALUES (343, 'U001', 'C002', 'CH001', 'video_finish', '{\"complete_rate\": 1.0, \"total_duration\": 180}', '2025-12-08 09:03:00');

-- ----------------------------
-- Table structure for user_knowledge_mastery
-- ----------------------------
DROP TABLE IF EXISTS `user_knowledge_mastery`;
CREATE TABLE `user_knowledge_mastery`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `knowledge_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `mastery_score` float NULL DEFAULT 0 COMMENT '掌握度（0-1）',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  CONSTRAINT `user_knowledge_mastery_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户知识点掌握度表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_knowledge_mastery
-- ----------------------------
INSERT INTO `user_knowledge_mastery` VALUES (1, 'U001', 'K001', 0.9);
INSERT INTO `user_knowledge_mastery` VALUES (2, 'U001', 'K002', 0.6);
INSERT INTO `user_knowledge_mastery` VALUES (3, 'U001', 'K003', 0.3);
INSERT INTO `user_knowledge_mastery` VALUES (4, 'U001', 'K004', 0.2);
INSERT INTO `user_knowledge_mastery` VALUES (5, 'U004', 'K001', 0.8);
INSERT INTO `user_knowledge_mastery` VALUES (6, 'U004', 'K002', 0.7);
INSERT INTO `user_knowledge_mastery` VALUES (7, 'U004', 'K006', 0.85);
INSERT INTO `user_knowledge_mastery` VALUES (8, 'U002', 'K008', 0.95);
INSERT INTO `user_knowledge_mastery` VALUES (9, 'U002', 'K009', 0.7);
INSERT INTO `user_knowledge_mastery` VALUES (10, 'U006', 'K011', 0.8);
INSERT INTO `user_knowledge_mastery` VALUES (11, 'U006', 'K012', 0.75);
INSERT INTO `user_knowledge_mastery` VALUES (12, 'U006', 'K013', 0.9);
INSERT INTO `user_knowledge_mastery` VALUES (13, 'U006', 'K014', 0.85);
INSERT INTO `user_knowledge_mastery` VALUES (14, 'U007', 'K011', 0.9);
INSERT INTO `user_knowledge_mastery` VALUES (15, 'U007', 'K012', 0.95);
INSERT INTO `user_knowledge_mastery` VALUES (16, 'U007', 'K013', 0.7);
INSERT INTO `user_knowledge_mastery` VALUES (17, 'U008', 'K001', 0.9);
INSERT INTO `user_knowledge_mastery` VALUES (18, 'U008', 'K002', 0.8);
INSERT INTO `user_knowledge_mastery` VALUES (19, 'U008', 'K017', 0.75);
INSERT INTO `user_knowledge_mastery` VALUES (20, 'U009', 'K003', 0.85);
INSERT INTO `user_knowledge_mastery` VALUES (21, 'U009', 'K004', 0.7);
INSERT INTO `user_knowledge_mastery` VALUES (22, 'U009', 'K020', 0.8);
INSERT INTO `user_knowledge_mastery` VALUES (23, 'U010', 'K018', 0.7);
INSERT INTO `user_knowledge_mastery` VALUES (24, 'U010', 'K019', 0.6);
INSERT INTO `user_knowledge_mastery` VALUES (25, 'U010', 'K017', 0.9);
INSERT INTO `user_knowledge_mastery` VALUES (26, 'U013', 'K008', 0.9);
INSERT INTO `user_knowledge_mastery` VALUES (27, 'U013', 'K009', 0.8);
INSERT INTO `user_knowledge_mastery` VALUES (28, 'U013', 'K022', 0.75);
INSERT INTO `user_knowledge_mastery` VALUES (29, 'U014', 'K023', 0.85);
INSERT INTO `user_knowledge_mastery` VALUES (30, 'U014', 'K024', 0.7);
INSERT INTO `user_knowledge_mastery` VALUES (31, 'U014', 'K025', 0.8);
INSERT INTO `user_knowledge_mastery` VALUES (32, 'U017', 'K010', 0.9);
INSERT INTO `user_knowledge_mastery` VALUES (33, 'U017', 'K011', 0.8);
INSERT INTO `user_knowledge_mastery` VALUES (34, 'U017', 'K027', 0.75);
INSERT INTO `user_knowledge_mastery` VALUES (35, 'U018', 'K028', 0.85);
INSERT INTO `user_knowledge_mastery` VALUES (36, 'U018', 'K029', 0.7);
INSERT INTO `user_knowledge_mastery` VALUES (37, 'U018', 'K030', 0.8);
INSERT INTO `user_knowledge_mastery` VALUES (38, 'U019', 'K011', 0.9);
INSERT INTO `user_knowledge_mastery` VALUES (39, 'U019', 'K012', 0.8);
INSERT INTO `user_knowledge_mastery` VALUES (40, 'U019', 'K032', 0.75);
INSERT INTO `user_knowledge_mastery` VALUES (41, 'U020', 'K033', 0.85);
INSERT INTO `user_knowledge_mastery` VALUES (42, 'U020', 'K034', 0.7);
INSERT INTO `user_knowledge_mastery` VALUES (43, 'U020', 'K035', 0.8);

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `user_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户唯一ID',
  `username` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户名',
  `favorite_domain` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '偏好领域',
  `created_at` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES ('U001', '张三', 'Python', '2025-12-07 20:54:02');
INSERT INTO `users` VALUES ('U002', '李四', 'Java', '2025-12-07 20:54:02');
INSERT INTO `users` VALUES ('U003', '王五', 'MySQL', '2025-12-07 20:54:02');
INSERT INTO `users` VALUES ('U004', '赵六', 'Python', '2025-12-07 20:54:02');
INSERT INTO `users` VALUES ('U005', '钱七', 'Java', '2025-12-07 20:54:02');
INSERT INTO `users` VALUES ('U006', '孙八', '文学', '2025-12-07 21:14:17');
INSERT INTO `users` VALUES ('U007', '周九', '文学', '2025-12-07 21:14:17');
INSERT INTO `users` VALUES ('U008', '吴十', 'Python', '2025-12-07 21:24:21');
INSERT INTO `users` VALUES ('U009', '郑十一', 'Python', '2025-12-07 21:24:21');
INSERT INTO `users` VALUES ('U010', '王十二', 'Python', '2025-12-07 21:24:21');
INSERT INTO `users` VALUES ('U011', '冯十三', 'Python', '2025-12-07 21:24:21');
INSERT INTO `users` VALUES ('U012', '陈十四', 'Python', '2025-12-07 21:24:21');
INSERT INTO `users` VALUES ('U013', '褚十五', 'Java', '2025-12-07 21:24:21');
INSERT INTO `users` VALUES ('U014', '卫十六', 'Java', '2025-12-07 21:24:21');
INSERT INTO `users` VALUES ('U015', '蒋十七', 'Java', '2025-12-07 21:24:21');
INSERT INTO `users` VALUES ('U016', '沈十八', 'Java', '2025-12-07 21:24:21');
INSERT INTO `users` VALUES ('U017', '韩十九', 'MySQL', '2025-12-07 21:24:21');
INSERT INTO `users` VALUES ('U018', '杨二十', 'MySQL', '2025-12-07 21:24:21');
INSERT INTO `users` VALUES ('U019', '朱二一', '文学', '2025-12-07 21:24:21');
INSERT INTO `users` VALUES ('U020', '秦二二', '文学', '2025-12-07 21:24:21');

SET FOREIGN_KEY_CHECKS = 1;
