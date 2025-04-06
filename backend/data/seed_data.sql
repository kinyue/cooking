-- Sample data for the recipes table

-- Recipe 1: 麻婆豆腐 (Mapo Tofu)
INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
VALUES (
    '麻婆豆腐',
    '一道经典的川菜，以麻、辣、烫、香、酥、嫩、鲜、活八字箴言为其特色。',
    '[{"name": "嫩豆腐", "quantity": "1块"}, {"name": "牛肉末", "quantity": "50克"}, {"name": "豆瓣酱", "quantity": "1汤匙"}, {"name": "豆豉", "quantity": "1茶匙"}, {"name": "姜末", "quantity": "1茶匙"}, {"name": "蒜末", "quantity": "1茶匙"}, {"name": "花椒粉", "quantity": "适量"}, {"name": "辣椒粉", "quantity": "适量"}, {"name": "葱花", "quantity": "适量"}, {"name": "水淀粉", "quantity": "适量"}, {"name": "食用油", "quantity": "适量"}, {"name": "盐", "quantity": "少许"}]',
    '["1. 豆腐切小块，放入加盐的沸水中焯烫一下捞出沥干。", "2. 锅中放油烧热，下牛肉末炒散变色。", "3. 加入豆瓣酱、豆豉、姜末、蒜末炒出红油。", "4. 加入适量清水或高汤，烧沸。", "5. 下入豆腐块，轻轻推匀，煮2-3分钟。", "6. 加入少许盐（豆瓣酱有咸味），淋入水淀粉勾芡。", "7. 起锅前撒上花椒粉、辣椒粉和葱花即可。"]',
    'images/mapo_tofu.jpg', -- Assuming images are stored relative to some base path
    '["家常菜", "川菜", "麻辣", "下饭菜", "简单"]',
    '简单',
    '川菜',
    10,
    15,
    2
);

-- Recipe 2: 红烧排骨 (Braised Pork Ribs)
INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
VALUES (
    '红烧排骨',
    '色泽红亮，口味咸甜适中，是深受大众喜爱的家常菜。',
    '[{"name": "猪肋排", "quantity": "500克"}, {"name": "冰糖", "quantity": "30克"}, {"name": "生抽", "quantity": "2汤匙"}, {"name": "老抽", "quantity": "1汤匙"}, {"name": "料酒", "quantity": "1汤匙"}, {"name": "姜片", "quantity": "3片"}, {"name": "葱段", "quantity": "2段"}, {"name": "八角", "quantity": "1个"}, {"name": "桂皮", "quantity": "1小块"}, {"name": "食用油", "quantity": "适量"}, {"name": "开水", "quantity": "适量"}]',
    '["1. 排骨冷水下锅，加料酒焯水后捞出洗净。", "2. 锅中放少许油，放入冰糖小火炒出糖色。", "3. 下入排骨翻炒均匀上色。", "4. 加入姜片、葱段、八角、桂皮炒香。", "5. 烹入料酒，加入生抽、老抽翻炒均匀。", "6. 加入没过排骨的开水，大火烧开后转小火炖煮40-60分钟。", "7. 大火收汁至汤汁浓稠即可。"]',
    'images/braised_ribs.jpg',
    '["家常菜", "本帮菜", "咸甜", "中等"]',
    '中等',
    '家常菜',
    15,
    60,
    3
);

-- Recipe 3: 西红柿炒鸡蛋 (Scrambled Eggs with Tomatoes)
INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
VALUES (
    '西红柿炒鸡蛋',
    '简单快手、营养丰富的国民家常菜。',
    '[{"name": "西红柿", "quantity": "2个"}, {"name": "鸡蛋", "quantity": "3个"}, {"name": "葱花", "quantity": "适量"}, {"name": "盐", "quantity": "适量"}, {"name": "糖", "quantity": "少许"}, {"name": "食用油", "quantity": "适量"}]',
    '["1. 西红柿洗净切块，鸡蛋打散备用。", "2. 锅中放油烧热，倒入蛋液炒熟盛出。", "3. 锅中留底油，放入葱花爆香。", "4. 下入西红柿块翻炒至软烂出汁。", "5. 加入炒好的鸡蛋，翻炒均匀。", "6. 加入盐和少许糖调味，炒匀即可出锅。"]',
    'images/tomato_eggs.jpg',
    '["家常菜", "快手菜", "简单", "酸甜"]',
    '简单',
    '家常菜',
    5,
    10,
    2
);


-- Recipe 4: 宫保鸡丁 (Kung Pao Chicken)
INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
VALUES (
    '宫保鸡丁',
    '一道闻名中外的特色传统名菜。',
    '[{"name": "鸡胸肉", "quantity": "200克"}, {"name": "花生米", "quantity": "50克"}, {"name": "干辣椒", "quantity": "10克"}, {"name": "花椒", "quantity": "5克"}, {"name": "葱段", "quantity": "15克"}, {"name": "姜片", "quantity": "5克"}, {"name": "蒜末", "quantity": "5克"}, {"name": "料酒", "quantity": "10毫升"}, {"name": "酱油", "quantity": "10毫升"}, {"name": "醋", "quantity": "15毫升"}, {"name": "糖", "quantity": "10克"}, {"name": "淀粉", "quantity": "5克"}, {"name": "食用油", "quantity": "适量"}]',
    '["1. 鸡胸肉切丁，用料酒、酱油、淀粉腌制10分钟。", "2. 干辣椒切段，去籽。", "3. 锅中放油烧热，下花生米炸至酥脆捞出。", "4. 锅中留底油，下花椒、干辣椒炒香。", "5. 下入鸡丁翻炒至变色。", "6. 加入葱段、姜片、蒜末炒香。", "7. 调入酱油、醋、糖，翻炒均匀。", "8. 倒入花生米，翻炒均匀即可。"]',
    'images/kung_pao_chicken.jpg',
    '["家常菜", "川菜", "香辣", "中等"]',
    '中等',
    '川菜',
    15,
    20,
    2
);

-- Recipe 5: 鱼香肉丝 (Yu Xiang Rou Si)
INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
VALUES (
    '鱼香肉丝',
    '具有咸、酸、甜、辣等多种风味的经典川菜。',
    '[{"name": "猪里脊肉", "quantity": "200克"}, {"name": "木耳", "quantity": "50克"}, {"name": "胡萝卜", "quantity": "50克"}, {"name": "青椒", "quantity": "50克"}, {"name": "葱姜蒜末", "quantity": "适量"}, {"name": "豆瓣酱", "quantity": "15克"}, {"name": "酱油", "quantity": "10毫升"}, {"name": "醋", "quantity": "15毫升"}, {"name": "糖", "quantity": "10克"}, {"name": "淀粉", "quantity": "5克"}, {"name": "食用油", "quantity": "适量"}]',
    '["1. 猪里脊肉切丝，用淀粉、料酒腌制10分钟。", "2. 木耳、胡萝卜、青椒切丝。", "3. 葱姜蒜切末。", "4. 锅中放油烧热，下肉丝翻炒至变色。", "5. 加入豆瓣酱炒出红油。", "6. 加入木耳、胡萝卜、青椒翻炒均匀。", "7. 调入酱油、醋、糖，翻炒均匀。", "8. 加入葱姜蒜末炒香即可。"]',
    'images/yu_xiang_rou_si.jpg',
    '["家常菜", "川菜", "鱼香", "中等"]',
    '中等',
    '川菜',
    20,
    25,
    2
);

-- Recipe 6: 可乐鸡翅 (Cola Chicken Wings)
INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
VALUES (
    '可乐鸡翅',
    '香甜可口，做法简单的家常菜。',
    '[{"name": "鸡翅", "quantity": "500克"}, {"name": "可乐", "quantity": "330毫升"}, {"name": "姜片", "quantity": "3片"}, {"name": "葱段", "quantity": "2段"}, {"name": "酱油", "quantity": "10毫升"}, {"name": "食用油", "quantity": "适量"}]',
    '["1. 鸡翅洗净，焯水。", "2. 锅中放油烧热，下鸡翅煎至两面金黄。", "3. 加入姜片、葱段炒香。", "4. 倒入可乐和酱油，大火烧开转小火炖煮20分钟。", "5. 大火收汁至汤汁浓稠即可。"]',
    'images/cola_chicken_wings.jpg',
    '["家常菜", "快手菜", "简单", "甜"]',
    '简单',
    '家常菜',
    5,
    25,
    3
);

-- Recipe 7: 清蒸鲈鱼 (Steamed Sea Bass)
INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
VALUES (
    '清蒸鲈鱼',
    '肉质鲜嫩，味道清淡鲜美，是宴客佳品。',
    '[{"name": "鲈鱼", "quantity": "1条"}, {"name": "葱", "quantity": "适量"}, {"name": "姜", "quantity": "适量"}, {"name": "蒸鱼豉油", "quantity": "适量"}, {"name": "料酒", "quantity": "1汤匙"}, {"name": "食用油", "quantity": "适量"}]',
    '["1. 鲈鱼处理干净，在鱼身两侧划几刀，抹上料酒腌制10分钟。", "2. 葱姜切丝，一部分铺在盘底，一部分塞入鱼肚和鱼身刀口处。", "3. 将鱼放入蒸锅，大火蒸8-10分钟（根据鱼的大小调整）。", "4. 蒸好后取出，倒掉盘中的汤汁，去掉葱姜丝。", "5. 在鱼身上重新铺上新的葱姜丝。", "6. 淋上蒸鱼豉油。", "7. 锅中烧热油，淋在葱姜丝上即可。"]',
    'images/steamed_sea_bass.jpg',
    '["家常菜", "粤菜", "清淡", "鲜美", "简单"]',
    '简单',
    '粤菜',
    15,
    10,
    3
);

-- Recipe 8: 糖醋里脊 (Sweet and Sour Pork Tenderloin)
INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
VALUES (
    '糖醋里脊',
    '外酥里嫩，酸甜可口，深受儿童喜爱。',
    '[{"name": "猪里脊肉", "quantity": "300克"}, {"name": "鸡蛋", "quantity": "1个"}, {"name": "淀粉", "quantity": "适量"}, {"name": "番茄酱", "quantity": "3汤匙"}, {"name": "白醋", "quantity": "2汤匙"}, {"name": "糖", "quantity": "3汤匙"}, {"name": "盐", "quantity": "少许"}, {"name": "料酒", "quantity": "1茶匙"}, {"name": "食用油", "quantity": "适量"}]',
    '["1. 里脊肉切条，加盐、料酒、蛋清、淀粉抓匀腌制15分钟。", "2. 碗中加入番茄酱、白醋、糖、少许水和淀粉调成糖醋汁。", "3. 锅中放足量油烧至六成热，下入肉条炸至金黄酥脆捞出。", "4. 升高油温复炸一次，使肉条更酥脆。", "5. 锅留底油，倒入糖醋汁烧至浓稠。", "6. 下入炸好的里脊条快速翻炒均匀，使每条都裹上酱汁即可。"]',
    'images/sweet_sour_pork.jpg',
    '["家常菜", "鲁菜", "酸甜", "中等"]',
    '中等',
    '鲁菜',
    20,
    20,
    3
);

-- Recipe 9: 回锅肉 (Twice-Cooked Pork)
INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
VALUES (
    '回锅肉',
    '色泽红亮，肥而不腻，入口浓香，是川菜中的经典。',
    '[{"name": "五花肉", "quantity": "300克"}, {"name": "青蒜苗", "quantity": "100克"}, {"name": "豆瓣酱", "quantity": "1汤匙"}, {"name": "甜面酱", "quantity": "1茶匙"}, {"name": "豆豉", "quantity": "1茶匙"}, {"name": "姜片", "quantity": "3片"}, {"name": "料酒", "quantity": "1汤匙"}, {"name": "酱油", "quantity": "1茶匙"}, {"name": "糖", "quantity": "少许"}, {"name": "食用油", "quantity": "适量"}]',
    '["1. 五花肉冷水下锅，加姜片、料酒煮至八成熟，捞出晾凉切薄片。", "2. 青蒜苗洗净切段。", "3. 锅中放少许油，下入五花肉片煸炒至出油，边缘卷曲。", "4. 将肉片推至锅边，下入豆瓣酱、甜面酱、豆豉炒出红油。", "5. 与肉片混合翻炒均匀。", "6. 加入酱油、少许糖调味。", "7. 下入青蒜苗段快速翻炒至断生即可。"]',
    'images/twice_cooked_pork.jpg',
    '["家常菜", "川菜", "香辣", "下饭菜", "中等"]',
    '中等',
    '川菜',
    25,
    15,
    3
);

-- Recipe 10: 酸辣土豆丝 (Hot and Sour Potato Strips)
INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
VALUES (
    '酸辣土豆丝',
    '口感爽脆，酸辣开胃，是最受欢迎的家常小炒之一。',
    '[{"name": "土豆", "quantity": "2个"}, {"name": "干辣椒", "quantity": "5个"}, {"name": "花椒", "quantity": "1茶匙"}, {"name": "葱", "quantity": "适量"}, {"name": "姜", "quantity": "适量"}, {"name": "蒜", "quantity": "适量"}, {"name": "白醋", "quantity": "2汤匙"}, {"name": "盐", "quantity": "适量"}, {"name": "糖", "quantity": "少许"}, {"name": "食用油", "quantity": "适量"}]',
    '["1. 土豆去皮切细丝，放入清水中浸泡，洗去淀粉，捞出沥干。", "2. 干辣椒剪段，葱姜蒜切末。", "3. 锅中放油烧热，下花椒、干辣椒段爆香。", "4. 下入葱姜蒜末炒香。", "5. 下入土豆丝快速翻炒。", "6. 沿锅边淋入白醋，继续翻炒。", "7. 加入盐、少许糖调味。", "8. 翻炒至土豆丝断生即可。"]',
    'images/hot_sour_potato.jpg',
    '["家常菜", "快手菜", "素菜", "酸辣", "简单"]',
    '简单',
    '家常菜',
    10,
    5,
    2
);

-- Recipe 11: 地三鲜 (Di San Xian)
INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
VALUES (
    '地三鲜',
    '东北名菜，以土豆、茄子、青椒为主料，咸鲜味美。',
    '[{"name": "土豆", "quantity": "1个"}, {"name": "茄子", "quantity": "1个"}, {"name": "青椒", "quantity": "1个"}, {"name": "蒜末", "quantity": "适量"}, {"name": "酱油", "quantity": "2汤匙"}, {"name": "蚝油", "quantity": "1汤匙"}, {"name": "糖", "quantity": "1茶匙"}, {"name": "淀粉", "quantity": "适量"}, {"name": "食用油", "quantity": "适量"}]',
    '["1. 土豆、茄子去皮切滚刀块，青椒去籽切块。", "2. 茄子块加少许盐腌制10分钟，挤出水分，裹上薄薄一层干淀粉。", "3. 锅中放宽油烧至七成热，分别下入土豆块和茄子块炸至金黄捞出。", "4. 青椒块快速过油捞出。", "5. 碗中加入酱油、蚝油、糖、淀粉和少量水调成碗汁。", "6. 锅留底油，下蒜末爆香。", "7. 倒入碗汁烧至浓稠。", "8. 下入炸好的土豆、茄子和青椒块，快速翻炒均匀即可。"]',
    'images/di_san_xian.jpg',
    '["家常菜", "东北菜", "素菜", "咸鲜", "中等"]',
    '中等',
    '东北菜',
    15,
    20,
    3
);

-- Recipe 12: 水煮牛肉 (Shui Zhu Niu Rou - Poached Beef in Hot Chili Oil)
INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
VALUES (
    '水煮牛肉',
    '麻辣鲜香，肉片滑嫩，是川菜的代表作之一。',
    '[{"name": "牛肉", "quantity": "300克"}, {"name": "豆芽", "quantity": "100克"}, {"name": "青菜", "quantity": "100克"}, {"name": "豆瓣酱", "quantity": "2汤匙"}, {"name": "干辣椒", "quantity": "20克"}, {"name": "花椒", "quantity": "10克"}, {"name": "姜末", "quantity": "10克"}, {"name": "蒜末", "quantity": "20克"}, {"name": "料酒", "quantity": "1汤匙"}, {"name": "酱油", "quantity": "1汤匙"}, {"name": "淀粉", "quantity": "1汤匙"}, {"name": "鸡蛋清", "quantity": "1个"}, {"name": "盐", "quantity": "适量"}, {"name": "食用油", "quantity": "适量"}, {"name": "高汤或水", "quantity": "适量"}]',
    '["1. 牛肉切薄片，加料酒、酱油、盐、蛋清、淀粉抓匀腌制15分钟。", "2. 豆芽和青菜焯水后铺在碗底。", "3. 锅中放油烧热，下豆瓣酱炒出红油，加入姜末炒香。", "4. 加入高汤或水烧沸，加盐、酱油调味。", "5. 下入腌好的牛肉片，快速滑散煮熟。", "6. 将牛肉片和汤汁倒入铺好蔬菜的碗中。", "7. 在牛肉片上撒上干辣椒段、花椒、蒜末。", "8. 锅中烧热油（约100ml），淋在调料上即可。"]',
    'images/shui_zhu_niu_rou.jpg',
    '["家常菜", "川菜", "麻辣", "下饭菜", "复杂"]',
    '复杂',
    '川菜',
    20,
    25,
    3
);

-- Recipe 13: 蚂蚁上树 (Ma Yi Shang Shu - Ants Climbing a Tree)
INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
VALUES (
    '蚂蚁上树',
    '以粉丝和肉末为主料，形象得名，口感丰富。',
    '[{"name": "粉丝", "quantity": "100克"}, {"name": "猪肉末", "quantity": "100克"}, {"name": "豆瓣酱", "quantity": "1汤匙"}, {"name": "葱末", "quantity": "适量"}, {"name": "姜末", "quantity": "适量"}, {"name": "蒜末", "quantity": "适量"}, {"name": "酱油", "quantity": "1汤匙"}, {"name": "料酒", "quantity": "1茶匙"}, {"name": "糖", "quantity": "少许"}, {"name": "食用油", "quantity": "适量"}, {"name": "高汤或水", "quantity": "适量"}]',
    '["1. 粉丝用温水泡软。", "2. 锅中放油烧热，下入肉末炒散变色。", "3. 加入料酒、豆瓣酱、葱姜蒜末炒香。", "4. 加入酱油、糖和适量高汤或水烧沸。", "5. 下入泡软的粉丝，翻炒均匀，煮至汤汁被粉丝吸收。", "6. 起锅前撒上葱花即可。"]',
    'images/ma_yi_shang_shu.jpg',
    '["家常菜", "川菜", "咸鲜", "简单"]',
    '简单',
    '川菜',
    15,
    15,
    2
);

-- Recipe 14: 蒜蓉西兰花 (Garlic Broccoli)
INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
VALUES (
    '蒜蓉西兰花',
    '清淡爽口，营养丰富，制作简单。',
    '[{"name": "西兰花", "quantity": "1棵"}, {"name": "大蒜", "quantity": "5瓣"}, {"name": "盐", "quantity": "适量"}, {"name": "蚝油", "quantity": "1茶匙"}, {"name": "食用油", "quantity": "适量"}, {"name": "水淀粉", "quantity": "少许"}]',
    '["1. 西兰花掰成小朵，洗净，放入加盐和几滴油的沸水中焯烫1分钟捞出沥干。", "2. 大蒜切末。", "3. 锅中放油烧热，下入蒜末爆香。", "4. 下入焯好的西兰花翻炒均匀。", "5. 加入盐、蚝油调味。", "6. 淋入少许水淀粉勾薄芡即可。"]',
    'images/garlic_broccoli.jpg',
    '["家常菜", "素菜", "快手菜", "清淡", "简单"]',
    '简单',
    '家常菜',
    10,
    5,
    2
);

-- Recipe 15: 啤酒鸭 (Beer Duck)
INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
VALUES (
    '啤酒鸭',
    '鸭肉鲜嫩，带有啤酒的清香，风味独特。',
    '[{"name": "鸭子", "quantity": "半只"}, {"name": "啤酒", "quantity": "1罐"}, {"name": "姜片", "quantity": "5片"}, {"name": "蒜瓣", "quantity": "5瓣"}, {"name": "干辣椒", "quantity": "适量"}, {"name": "八角", "quantity": "2个"}, {"name": "桂皮", "quantity": "1小块"}, {"name": "酱油", "quantity": "2汤匙"}, {"name": "老抽", "quantity": "1汤匙"}, {"name": "冰糖", "quantity": "10克"}, {"name": "食用油", "quantity": "适量"}]',
    '["1. 鸭子斩块，冷水下锅焯水后捞出洗净。", "2. 锅中放少许油，下入鸭块煸炒至出油，表面微黄。", "3. 加入姜片、蒜瓣、干辣椒、八角、桂皮炒香。", "4. 加入酱油、老抽、冰糖翻炒上色。", "5. 倒入一罐啤酒，没过鸭块（不够可加少许水）。", "6. 大火烧开后转小火炖煮40-50分钟。", "7. 大火收汁至汤汁浓稠即可。"]',
    'images/beer_duck.jpg',
    '["家常菜", "荤菜", "香辣", "中等"]',
    '中等',
    '家常菜',
    20,
    60,
    4
);

-- Recipe 16: 葱油拌面 (Scallion Oil Noodles)
INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
VALUES (
    '葱油拌面',
    '简单快捷的家常面食，葱香浓郁。',
    '[{"name": "细面条", "quantity": "200克"}, {"name": "小葱", "quantity": "1把"}, {"name": "食用油", "quantity": "100毫升"}, {"name": "酱油", "quantity": "3汤匙"}, {"name": "老抽", "quantity": "1汤匙"}, {"name": "糖", "quantity": "1汤匙"}]',
    '["1. 小葱洗净切长段，葱白和葱绿分开。", "2. 锅中倒入食用油，冷油下入葱白段，小火慢炸。", "3. 炸至葱白变黄，下入葱绿段继续小火慢炸。", "4. 炸至葱段焦黄酥脆，捞出葱段（炸好的葱油留用）。", "5. 在炸好的葱油中加入酱油、老抽、糖，小火煮沸即成葱油酱汁。", "6. 另起锅烧水，煮熟面条捞出。", "7. 在面条上淋上葱油酱汁，放上炸好的葱段拌匀即可。"]',
    'images/scallion_oil_noodles.jpg',
    '["家常菜", "面食", "快手菜", "简单"]',
    '简单',
    '家常菜',
    5,
    20,
    1
);

-- Recipe 17: 扬州炒饭 (Yangzhou Fried Rice)
INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
VALUES (
    '扬州炒饭',
    '配料丰富，色彩鲜艳，米饭粒粒分明。',
    '[{"name": "米饭", "quantity": "2碗（隔夜饭佳）"}, {"name": "鸡蛋", "quantity": "2个"}, {"name": "虾仁", "quantity": "50克"}, {"name": "火腿丁", "quantity": "50克"}, {"name": "豌豆", "quantity": "30克"}, {"name": "胡萝卜丁", "quantity": "30克"}, {"name": "玉米粒", "quantity": "30克"}, {"name": "葱花", "quantity": "适量"}, {"name": "盐", "quantity": "适量"}, {"name": "料酒", "quantity": "少许"}, {"name": "食用油", "quantity": "适量"}]',
    '["1. 虾仁用料酒、少许盐腌制。豌豆、胡萝卜丁、玉米粒焯水。", "2. 鸡蛋打散。", "3. 锅中放油烧热，倒入蛋液炒散盛出。", "4. 锅留底油，下葱花爆香。", "5. 下入虾仁、火腿丁翻炒。", "6. 加入豌豆、胡萝卜丁、玉米粒翻炒均匀。", "7. 倒入米饭，用锅铲压散炒匀。", "8. 加入炒好的鸡蛋，翻炒均匀。", "9. 加入适量盐调味，炒匀即可。"]',
    'images/yangzhou_fried_rice.jpg',
    '["家常菜", "主食", "炒饭", "简单"]',
    '简单',
    '淮扬菜',
    15,
    10,
    2
);

-- Recipe 18: 干煸四季豆 (Dry-Fried Green Beans)
INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
VALUES (
    '干煸四季豆',
    '外焦里嫩，咸香微辣，非常下饭。',
    '[{"name": "四季豆", "quantity": "400克"}, {"name": "猪肉末", "quantity": "50克"}, {"name": "芽菜或冬菜", "quantity": "20克"}, {"name": "干辣椒", "quantity": "5个"}, {"name": "花椒", "quantity": "1茶匙"}, {"name": "姜末", "quantity": "适量"}, {"name": "蒜末", "quantity": "适量"}, {"name": "料酒", "quantity": "1茶匙"}, {"name": "酱油", "quantity": "1茶匙"}, {"name": "盐", "quantity": "少许"}, {"name": "糖", "quantity": "少许"}, {"name": "食用油", "quantity": "适量"}]',
    '["1. 四季豆掐去两头，撕掉老筋，掰成段，洗净沥干。", "2. 锅中放宽油烧至七成热，下入四季豆炸至表皮起皱，捞出控油。", "3. 锅留底油，下入肉末炒散变色，加入料酒。", "4. 加入干辣椒段、花椒、姜末、蒜末、芽菜炒香。", "5. 倒入炸好的四季豆翻炒均匀。", "6. 加入酱油、盐、糖调味，翻炒均匀即可。"]',
    'images/dry_fried_green_beans.jpg',
    '["家常菜", "川菜", "素菜", "香辣", "中等"]',
    '中等',
    '川菜',
    15,
    15,
    3
);

-- Recipe 19: 剁椒鱼头 (Steamed Fish Head with Diced Hot Red Peppers)
INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
VALUES (
    '剁椒鱼头',
    '鲜辣可口，是湘菜中的名菜。',
    '[{"name": "胖头鱼头", "quantity": "1个"}, {"name": "剁椒", "quantity": "100克"}, {"name": "葱", "quantity": "适量"}, {"name": "姜", "quantity": "适量"}, {"name": "蒜", "quantity": "适量"}, {"name": "料酒", "quantity": "2汤匙"}, {"name": "蒸鱼豉油", "quantity": "2汤匙"}, {"name": "食用油", "quantity": "适量"}, {"name": "盐", "quantity": "少许"}, {"name": "糖", "quantity": "少许"}]',
    '["1. 鱼头处理干净，从中间劈开但不要切断，抹上料酒和少许盐腌制15分钟。", "2. 姜切片，蒜切末，葱切花。", "3. 盘底铺上姜片，放上鱼头。", "4. 将剁椒均匀铺在鱼头上，加入蒜末、少许糖。", "5. 放入蒸锅，大火蒸12-15分钟。", "6. 取出鱼头，撒上葱花。", "7. 淋上蒸鱼豉油。", "8. 锅中烧热油，淋在葱花和剁椒上即可。"]',
    'images/steamed_fish_head_剁椒.jpg',
    '["家常菜", "湘菜", "鲜辣", "中等"]',
    '中等',
    '湘菜',
    20,
    15,
    4
);

-- Recipe 20: 麻辣香锅 (Mala Xiang Guo - Spicy Numbing Stir-fry Pot)
INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
VALUES (
    '麻辣香锅',
    '食材丰富，麻辣鲜香，自由搭配。',
    '[{"name": "各种蔬菜", "quantity": "适量（如藕片、土豆片、西兰花、木耳等）"}, {"name": "各种肉类/海鲜", "quantity": "适量（如午餐肉、肥牛卷、虾、鱼丸等）"}, {"name": "麻辣香锅底料", "quantity": "1包"}, {"name": "干辣椒", "quantity": "适量"}, {"name": "花椒", "quantity": "适量"}, {"name": "葱段", "quantity": "适量"}, {"name": "姜片", "quantity": "适量"}, {"name": "蒜瓣", "quantity": "适量"}, {"name": "食用油", "quantity": "适量"}, {"name": "白芝麻", "quantity": "少许"}]',
    '["1. 将所有食材处理好，不易熟的蔬菜和肉类提前焯水或过油。", "2. 锅中放油烧热，下葱姜蒜、干辣椒、花椒爆香。", "3. 加入麻辣香锅底料炒出红油。", "4. 按照食材易熟程度，依次下入处理好的食材翻炒。", "5. 翻炒均匀，确保所有食材都裹上酱料并炒熟。", "6. 起锅前撒上白芝麻即可。"]',
    'images/mala_xiang_guo.jpg',
    '["家常菜", "川菜", "麻辣", "自由搭配", "中等"]',
    '中等',
    '川菜',
    30,
    20,
    4
);

-- Recipe 21: 蛋挞 (Egg Tart)
INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
VALUES (
    '蛋挞',
    '酥皮香脆，内馅嫩滑，经典的港式甜点。',
    '[{"name": "蛋挞皮", "quantity": "12个（现成）"}, {"name": "淡奶油", "quantity": "100克"}, {"name": "牛奶", "quantity": "80克"}, {"name": "细砂糖", "quantity": "30克"}, {"name": "鸡蛋黄", "quantity": "2个"}, {"name": "炼乳", "quantity": "1茶匙（可选）"}]',
    '["1. 将淡奶油、牛奶、细砂糖、炼乳（如果用）倒入小锅中，小火加热搅拌至糖融化，离火晾凉。", "2. 鸡蛋黄打散。", "3. 将蛋黄液慢慢倒入晾凉的奶液中，边倒边搅拌均匀，制成挞水。", "4. 将挞水过筛，使其更细腻。", "5. 将挞水倒入蛋挞皮中，约八分满。", "6. 放入预热好的烤箱，200°C烤20-25分钟，至挞水凝固，表面出现焦斑即可。"]',
    'images/egg_tart.jpg',
    '["甜点", "烘焙", "港式", "简单"]',
    '简单',
    '粤菜',
    10,
    25,
    12
);

-- Recipe 22: 拔丝地瓜 (Basi Digua - Candied Sweet Potatoes)
INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
VALUES (
    '拔丝地瓜',
    '色泽金黄，外脆内软，香甜可口。',
    '[{"name": "红薯", "quantity": "500克"}, {"name": "白砂糖", "quantity": "100克"}, {"name": "食用油", "quantity": "适量"}]',
    '["1. 红薯去皮切滚刀块。", "2. 锅中放足量油烧至五成热，下入红薯块炸熟，表面金黄捞出。", "3. 锅留少许底油，放入白砂糖，小火慢炒。", "4. 不停搅拌，直至砂糖完全融化，变成浅琥珀色，泡沫由大变小。", "5. 迅速倒入炸好的红薯块，快速翻炒均匀，使糖浆均匀裹在红薯上。", "6. 立即出锅装盘（盘子提前抹油防粘），旁边放一碗凉开水，蘸水食用。"]',
    'images/basi_digua.jpg',
    '["甜点", "家常菜", "鲁菜", "甜", "中等"]',
    '中等',
    '鲁菜',
    10,
    15,
    3
);

-- Recipe 23: 叫花鸡 (Jiao Hua Ji - Beggar's Chicken)
INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
VALUES (
    '叫花鸡',
    '用荷叶和泥巴包裹煨烤而成，肉质酥烂，风味独特。',
    '[{"name": "嫩母鸡", "quantity": "1只"}, {"name": "猪肉丁", "quantity": "50克"}, {"name": "香菇丁", "quantity": "30克"}, {"name": "虾米", "quantity": "10克"}, {"name": "葱姜末", "quantity": "适量"}, {"name": "酱油", "quantity": "2汤匙"}, {"name": "料酒", "quantity": "1汤匙"}, {"name": "蚝油", "quantity": "1汤匙"}, {"name": "五香粉", "quantity": "少许"}, {"name": "盐", "quantity": "适量"}, {"name": "荷叶", "quantity": "2张"}, {"name": "黄泥或面粉", "quantity": "适量"}]',
    '["1. 鸡处理干净，用酱油、料酒、盐、五香粉内外抹匀腌制1小时。", "2. 锅中放油，炒香葱姜末，下入猪肉丁、香菇丁、虾米翻炒，加酱油、蚝油调味成馅料。", "3. 将馅料填入鸡腹中。", "4. 用荷叶将鸡包裹严实。", "5. 用和好的黄泥（或用面粉加水和成硬面团）将荷叶鸡均匀包裹起来。", "6. 放入预热好的烤箱或炭火中，用180°C左右的温度煨烤2-3小时。", "7. 取出敲开泥（或面壳），剥去荷叶即可食用。"]',
    'images/beggars_chicken.jpg',
    '["大菜", "苏菜", "咸鲜", "复杂"]',
    '复杂',
    '苏菜',
    90,
    180,
    4
);

-- Recipe 24: 佛跳墙 (Fo Tiao Qiang - Buddha Jumps Over the Wall)
INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
VALUES (
    '佛跳墙',
    '闽菜中的首席名菜，集多种珍贵食材于一坛，滋补养生。',
    '[{"name": "鲍鱼", "quantity": "适量"}, {"name": "海参", "quantity": "适量"}, {"name": "鱼翅", "quantity": "适量"}, {"name": "花胶", "quantity": "适量"}, {"name": "干贝", "quantity": "适量"}, {"name": "蹄筋", "quantity": "适量"}, {"name": "鸽子蛋", "quantity": "适量"}, {"name": "香菇", "quantity": "适量"}, {"name": "冬笋", "quantity": "适量"}, {"name": "高汤", "quantity": "适量"}, {"name": "绍兴酒", "quantity": "适量"}, {"name": "冰糖", "quantity": "少许"}, {"name": "盐", "quantity": "适量"}]',
    '["1. 将各种干货提前泡发处理好。", "2. 将处理好的食材分别焯水或过油。", "3. 取一佛跳墙专用坛，将食材按一定次序分层放入坛内。", "4. 加入高汤、绍兴酒、冰糖、盐等调味料。", "5. 用荷叶封住坛口，盖上坛盖。", "6. 将坛子放入蒸笼或隔水炖，小火慢煨数小时（通常4小时以上）。", "7. 煨至汤汁浓稠，食材软烂入味即可。"]',
    'images/fo_tiao_qiang.jpg',
    '["大菜", "闽菜", "滋补", "咸鲜", "非常复杂"]',
    '非常复杂',
    '闽菜',
    120, -- Prep time includes soaking time for dried ingredients
    240,
    6
);
