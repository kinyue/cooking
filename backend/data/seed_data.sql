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
