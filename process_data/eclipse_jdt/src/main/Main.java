package main;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.regex.*;
import org.eclipse.jdt.core.dom.ASTNode;
import net.sf.json.JSONObject;
import structure.MyASTNode;
import structure.MyMethodNode;

public class Main {
	public static List<File> fileList=new ArrayList<>();
	
	public static void main(String[] args)throws IOException{
		String dir = "C:\\Users\\Michael\\Desktop\\activemq-5.0.0";
		File fileDir=new File(dir);
		search(fileDir);
		
		for(File f:fileList) {
			BufferedReader reader=new BufferedReader(new FileReader(f));
			String tempString;
			List<String> content=new ArrayList<>();
			while((tempString=reader.readLine())!=null) {
				content.add(tempString.trim());
			}
			reader.close();
			int num=content.size();
			ArrayList[] data=new ArrayList[num];
			for(int i=0;i<data.length;i++) {
				data[i]=new ArrayList();
			}
			
			ASTGenerator astGenerator=new ASTGenerator(f);
			List<MyMethodNode> methodNodeList =astGenerator.getMethodNodeList();
			for(MyMethodNode m:methodNodeList) {
				ASTtoNodeType(m,data);
			}
			System.out.println("Finished!");
			
		}
	}
	
	private static void search(File file) {
		File[] fs = file.listFiles();
		for (File f : fs) {
			if (f.isDirectory())
				search(f);
			if (f.isFile() && f.getName().toLowerCase().endsWith(".java"))
				fileList.add(f);
		}
	}
	
	@SuppressWarnings("unchecked")
	public static void ASTtoNodeType(MyMethodNode m, ArrayList[] data) {
		for(MyASTNode mn:m.nodeList) {
			String nodeType=ASTNode.nodeClassForType(mn.astNode.getNodeType()).getName().replace("org.eclipse.jdt.core.dom.", "");
			int startLine=mn.startLineNum;
			int endLine=mn.endLineNum;
			
			if(nodeType.equals("Javadoc"))continue;
			
			for(int i=startLine;i<=endLine;i++) {
				//jdt解析代码的时候下标从1开始计算，把对应的代码行AST转换成以0为下标开始的数组形式容易理解
				data[i-1].add(nodeType);
			}
		}
	}

}
