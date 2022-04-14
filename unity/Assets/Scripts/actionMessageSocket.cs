using UnityEngine;
using System;
using System.Globalization;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Collections.Generic;
using TMPro;

public class actionMessageSocket : MonoBehaviour
{
    Thread mThread; // thread to manage communication with python
    public string connectionIP = "127.0.0.1";
    public int connectionPort = 25002;
    IPAddress localAdd;
    TcpListener listener;
    TcpClient client;
    bool running;
    string requestedAction;
    RobotStatus currentState;
    IDictionary<string, RobotStatus> messageStateMapper = new Dictionary<string, RobotStatus>();
    Animator animator;
    void receiveActionMessage()
    {
        NetworkStream nwStream = client.GetStream();
        byte[] buffer = new byte[client.ReceiveBufferSize];

        //---receiving Data from the Host----
        int bytesRead = nwStream.Read(buffer, 0, client.ReceiveBufferSize); //Getting data in Bytes from Python
        string dataReceived = Encoding.UTF8.GetString(buffer, 0, bytesRead); //Converting byte data to string

        if (dataReceived != null)
        {
            requestedAction = dataReceived;
            byte[] responseBuffer = Encoding.ASCII.GetBytes("Received");
            nwStream.Write(responseBuffer, 0, responseBuffer.Length);
        }
    }
    void GetInfo()
    {
        localAdd = IPAddress.Parse(connectionIP);
        listener = new TcpListener(IPAddress.Any, connectionPort);
        listener.Start();

        client = listener.AcceptTcpClient();

        running = true;
        while (running)
        {
            receiveActionMessage();
        }

        listener.Stop();
    }

    private void initialiseStateMapper()
    {
        messageStateMapper.Add("stop",RobotStatus.Idle);
        messageStateMapper.Add("horizontal-attack",RobotStatus.HorizontalAttack);
        messageStateMapper.Add("kick-attack",RobotStatus.KickAttack);
        messageStateMapper.Add("combo-attack-1",RobotStatus.ComboAttack);
        messageStateMapper.Add("combo-attack-2",RobotStatus.ComboAttack2);
    }

    private void Start()
    {
        //start in idle state
        currentState = RobotStatus.Idle;
        animator = GetComponent<Animator>();
        //initialise message state mapper
        initialiseStateMapper();
        //Start thread for communication with python
        ThreadStart ts = new ThreadStart(GetInfo);
        mThread = new Thread(ts);
        mThread.Start();
        print("Listening for action messages");
    }

    private void Update()
    {
        //refer to value of requestedAction and update object state
        if (requestedAction != null)
        {
            print("Requested action="+requestedAction);
            
            if(messageStateMapper.ContainsKey(requestedAction))
            {
                if(currentState == RobotStatus.Idle)
                {
                    currentState = messageStateMapper[requestedAction];
                    if (currentState == RobotStatus.HorizontalAttack)
                    {
                        animator.SetBool("attack_horizontal",true);
                    }
                    else if(currentState == RobotStatus.KickAttack)
                    {
                        animator.SetBool("attack_kick",true);
                    }
                    else if(currentState == RobotStatus.ComboAttack)
                    {
                        animator.SetBool("attack_combo_v1",true);
                    }
                    else if(currentState == RobotStatus.ComboAttack2)
                    {
                        animator.SetBool("attack_combo_v2",true);
                    }
                    requestedAction = null;
                }
                else if(requestedAction.Equals("stop"))
                {
                    if (currentState == RobotStatus.HorizontalAttack)
                    {
                        animator.SetBool("attack_horizontal",false);
                    }
                    else if(currentState == RobotStatus.KickAttack)
                    {
                        animator.SetBool("attack_kick",false);
                    }
                    else if(currentState == RobotStatus.ComboAttack)
                    {
                        animator.SetBool("attack_combo_v1",false);
                    }
                    else if(currentState == RobotStatus.ComboAttack2)
                    {
                        animator.SetBool("attack_combo_v2",false);
                    }
                    //set current state to idle
                    currentState = RobotStatus.Idle;                    
                }
            }
            else
            {
                print("Action not found");
            }
        }
    }

    private void Stop()
    {
        listener.Stop();
        client.Close();
    }
}

public enum RobotStatus
{
    Idle,
    HorizontalAttack,
    KickAttack,
    ComboAttack,
    ComboAttack2
}