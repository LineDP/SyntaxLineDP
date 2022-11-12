package main;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.List;

public class ExtractContent {
	
	public static List<File> fileList = new ArrayList<>();
	
	public static void main(String[] args) throws IOException {
		String dir = "E:\\java-project\\vuze-master";  // 需要遍历的路径
		File fileDir = new File(dir);  // 获取路径的file对象
		search(fileDir);
		FileOutputStream out = new FileOutputStream(dir + "\\content.txt");
		BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(out));
		for(File f:fileList) {
			BufferedReader reader = new BufferedReader(new FileReader(f));
			String tempString;
			while ((tempString = reader.readLine()) != null) {
				writer.write(tempString + '\n');
			}
			reader.close();
		}
		try {
            if (writer != null) {
                writer.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
	}
	
	private static void search(File file) {
		File[] fs = file.listFiles();
		for(File f:fs) {
			if(f.isDirectory())
				search(f);
			if(f.isFile() && f.getName().toLowerCase().endsWith(".java"))
				fileList.add(f);
		}
	}
}