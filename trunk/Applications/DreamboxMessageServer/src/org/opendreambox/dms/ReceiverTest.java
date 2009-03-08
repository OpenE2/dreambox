package org.opendreambox.dms;

import java.net.ServerSocket;
import java.io.IOException;

public class ReceiverTest {
	public static void main(String[] args) throws IOException {
		ServerSocket serverSocket = new ServerSocket(9000);
		System.out.println("1");
		Receiver receiver = new Receiver(serverSocket.accept());
	}
}
